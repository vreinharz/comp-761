#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
#define A 0
#define C 1
#define G 2
#define U 3
#define inf 100000000

char rangeStart ='!';
char rangeEnd = '~' ;

//string inputName = "RF.tree";
int table[4][4]={{9,214,131,223},{214,0,225,131},{131,225,0,214},{223,131,214,9}};
ofstream out("output.txt");

class score{
public:
	int scr[4];
};
class profile{
public:
	profile(){ a=0; c=0; g=0; u=0;}
	float a,c,g,u;
};
class node{
public:
	node (){
		child = NULL;
		rightBrother = NULL;
		set = false;
	}
	string sequence;
	string name;
	bool set;
	vector<profile> pr;
	vector<score> scr;
	int father;
	int me;
	node *child;
	node *rightBrother;
	vector <node*>childs;
};

node* makeTree(string str, node* root){
	int * par;
	int i, counter = 0 ,start, end ;
	if (root == NULL)
		root = new node();
	string newStr;
	vector<bool> flags;
	vector<int> op,cp;
	par = new int[str.size()];
	for (i=0 ; i < str.size(); i++){
		if(str[i] == '('){
			par[i] = counter;
			counter ++;
			flags.push_back(false);
			op.push_back(i);
		}
		else 
			par[i] = -1;
	}
	for (i=0 ; i < str.size(); i++){
		if(str[i]==')'){ 
			cp.push_back(i);
		}
	}
	for (i=0 ; i < cp.size(); i++){
		int j=0;
		while(op[j]<cp[i]){
			j++;
			if(j==op.size())
				break;
		}
		j--;
		while(flags[j]==true)
			j--;
		flags[j]=true;
		par[cp[i]]=par[op[j]];
	}
	if(op.size()==0){
		root->child=NULL;
		root->sequence= str;
		return root;
	}
	if(op.size()!=cp.size())
		cout<<"shit again"<<endl;
	bool flag = false;
	counter = 1;
	for ( i = 0 ; i < str.size(); i++){
		if(par[i]==0){
			flag = true;
			start = i;
			i++;
			while(par[i]!=0){
				i++;
			}
			end = i;
			newStr.clear();
			newStr = str.substr(0,start);
			if(!newStr.empty()){
				root->sequence = newStr;
				newStr = str.substr(start,str.size()-start);
				node * brother = makeTree(newStr,NULL);
				if(brother)
					root->rightBrother=brother;
				return root;
			}
			else{
				newStr = str.substr(start+1,end-start-1);
				node* child= makeTree(newStr,NULL);
				if(child)
					root->child=child;
				if(!newStr.empty()){
				newStr=str.substr(end+1,str.size()-end);
				node * brother = makeTree(newStr,NULL);
				if(brother)
					root->rightBrother=brother;
				}
				return root;

			}
		}
			
	}

	return NULL;
}
void reConstruct(node *root){
	if(root == NULL){
		return;
	}
	if(root->child!=NULL){
		node *temp;
		temp = root->child;
		while(temp!=NULL){
			if(temp->child!=NULL||!temp->sequence.empty())
				root->childs.push_back(temp);
			temp=temp->rightBrother;
		}
	}
	reConstruct(root->child);
	reConstruct(root->rightBrother);
}
int name = 0;
void rephrase(node *root){
	if(root == NULL)
		return;
	if(root->child==NULL){
		return;
	}
	else
	{
		for(int i=0 ; i<root->childs.size(); i++){
			if(root->childs[i]->child==NULL && root->childs[i]->sequence.length()<10){
				root->childs.erase(root->childs.begin()+i);
				i--;
			}
			else{
				name ++;
				root->childs[i]->father=root->me;
				root->childs[i]->me=name;
				rephrase(root->childs[i]);
			}
		}
	}
}
void setLeaves(node *root){
	string str;
	if(root == NULL)
		return;
	if(root->child==NULL){
		return;
	}
	else
	{
		for(int i=0 ; i<root->childs.size(); i++){
			if(root->childs[i]->child==NULL && root->childs[i]->sequence.length()<10){
				root->childs.erase(root->childs.begin()+i);
				i--;
			}
			else{
				if(!root->childs[i]->sequence.empty()){
					str = root->childs[i]->sequence;
					int index = str.find("|");
					if(index < 0 )
						continue;
					else{
						str.erase(str.begin(),str.begin()+index+1);
						index = str.find("|");
						str.erase(str.begin(),str.begin()+index+1);
						index = str.find(",");
						if(index>=0){
							root->childs[i]->sequence = str.substr(0,index);
							str.erase(str.begin(),str.begin()+index+1);
							while(!str.empty()){
								index = str.find("|");
								str.erase(str.begin(),str.begin()+index+1);
								index = str.find("|");
								str.erase(str.begin(),str.begin()+index+1);
								index = str.find(",");
								node * newChild = new node();
								if(index>=0){
									newChild->sequence = str.substr(0,index);
									newChild->father=root->me;
									name ++;
									newChild->me=name;
									root->childs.push_back(newChild);
									str.erase(str.begin(),str.begin()+index+1);
								}
								else{
									newChild->sequence = str;
									newChild->father=root->me;
									name ++;
									newChild->me=name;
									root->childs.push_back(newChild);
									str.clear();
								}

							}
						}
						else
							root->childs[i]->sequence = str;
					}
				}
				setLeaves(root->childs[i]);
			}
		}
	}
}
void makingScore(node *root){
	int i;
	score *tempScr;
	profile * tempP;
	if(root==NULL)
		return;
	if(!root->sequence.empty()){
		for (i = 0 ; i < root->sequence.size() ; i++){
			tempScr = new score;
			tempP = new profile();
			tempScr->scr[0] = inf;
			tempScr->scr[1] = inf;
			tempScr->scr[2] = inf;
			tempScr->scr[3] = inf;
			
			if(root->sequence[i]=='A'){
				tempScr->scr[0] = 0;
				root->scr.push_back(*tempScr);
				tempP->a=1;
				root->pr.push_back(*tempP);
			}
			if(root->sequence[i]=='C'){
				tempScr->scr[1] = 0;
				root->scr.push_back(*tempScr);
				tempP->c=1;
				root->pr.push_back(*tempP);
			}
			if(root->sequence[i]=='G'){
				tempScr->scr[2] = 0;
				root->scr.push_back(*tempScr);
				tempP->g=1;
				root->pr.push_back(*tempP);
			}
			if(root->sequence[i]=='U'){
				tempScr->scr[3] = 0;
				root->scr.push_back(*tempScr);
				tempP->u=1;
				root->pr.push_back(*tempP);
			}
		}
		root->set=true;
	}
	
	for(i = 0 ; i < root->childs.size();i++)
		makingScore(root->childs[i]);

}
bool checkNode(node *root){
	if(root ==NULL)
		return true;
	for(int i=0; i<root->childs.size() ; i++)
		if(root->childs[i]->set == false)
			return false;
	return true;
}
node * findNode(node * root){
	if(root == NULL)
		return NULL;
	if(checkNode(root)&&!root->set)
		return root;
	for( int i = 0 ; i < root->childs.size() ; i++){
		if(checkNode(root->childs[i])&&!root->childs[i]->set)
			return root->childs[i];
		else{
			if( findNode(root->childs[i]))
				return findNode(root->childs[i]);
		}
	}
		return NULL;
}
score calMin(score scr){
	score newScr;
	int min;
	for(int i = 0 ; i < 4 ; i ++ ) {
		min=inf;
		for(int j = 0 ; j < 4 ; j++){
			if(min>scr.scr[j]+table[j][i])
				min = scr.scr[j]+table[j][i];
		}
		newScr.scr[i]= min;

	}
	return newScr;
}
void sankoff(node*root){
	node * crnt;
	while(root->set!=true){
		crnt = findNode(root);
		score * scr;
		for(int i = 0 ; i < crnt->child->scr.size();i++){
			scr = new score();
			score scrSum;
			scrSum.scr[0]=0;
			scrSum.scr[1]=0;
			scrSum.scr[2]=0;
			scrSum.scr[3]=0;
			for(int j = 0 ; j < crnt->childs.size();j++){
				*scr = calMin(crnt->childs[j]->scr[i]);
				scrSum.scr[0]+=scr->scr[0];
				scrSum.scr[1]+=scr->scr[1];
				scrSum.scr[2]+=scr->scr[2];
				scrSum.scr[3]+=scr->scr[3];

			}
			crnt->scr.push_back(scrSum);
		}
		float sum;
		profile *p;
		for(int i =0 ; i < crnt->scr.size();i++){
			sum = 0 ;
			p = new profile();
			sum = crnt->scr[i].scr[0]+crnt->scr[i].scr[1]+crnt->scr[i].scr[2]+crnt->scr[i].scr[3];
			p->a = ((float)crnt->scr[i].scr[0])/((float)sum);
			p->c = ((float)crnt->scr[i].scr[1])/((float)sum);
			p->g = ((float)crnt->scr[i].scr[2])/((float)sum);
			p->u = ((float)crnt->scr[i].scr[3])/((float)sum);
			crnt->pr.push_back(*p);
		}
		crnt->set = true;

	}
	return;
}
void print(node *root){
	if(root==NULL)
		return;
	int i,j,newChar;
	int range = (int)rangeEnd - (int)rangeStart;
	char tempChar;
	out <<">"<<root->me;
	for( i = 0 ; i < root->childs.size();i++)
		out<<"+"<<root->childs[i]->me;
	out<<endl;
		for(i=0;i<root->pr.size();i++){
			newChar = (int)(root->pr[i].a*range);
			tempChar = (char)(newChar+(int)rangeStart);
			out<<tempChar;
		}
		out<<endl;
		for(i=0;i<root->pr.size();i++){
			newChar = (int)(root->pr[i].c*range);
			tempChar = (char)(newChar+(int)rangeStart);
			out<<tempChar;
		}
		out<<endl;
		for(i=0;i<root->pr.size();i++){
			newChar = (int)(root->pr[i].g*range);
			tempChar = (char)(newChar+(int)rangeStart);
			out<<tempChar;
		}
		out<<endl;
		for(i=0;i<root->pr.size();i++){
			newChar = (int)(root->pr[i].u*range);
			tempChar = (char)(newChar+(int)rangeStart);
			out<<tempChar;
		}
		out<<endl;
	for( i = 0 ; i < root->childs.size();i++)
		print(root->childs[i]);
}
int main(int argc,char*argv[]){
	string mainStr;
	char *temp;
	temp = new char[50000];
	string inputName(argv[1]);
	ifstream in(inputName.c_str());
	in.getline(temp,50000);
	mainStr = temp;
	delete[] temp;
	node *root = new node;
	makeTree(mainStr,root);
	reConstruct(root);
	root->me=0;
	rephrase(root);
	setLeaves(root);
	makingScore(root);
	sankoff(root);
	print(root);
	out.close();
	return 0;
}