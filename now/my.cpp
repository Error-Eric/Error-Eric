#include<iostream>
#include<algorithm>
#include<vector>
#include<numeric>
#include<map>
//#include<ranges>
using namespace std;
const int _= 3e5 + 5;
int n, m, a[_], o, cu=1, cv=0;
map<int, int> tosmall, questions;
class fwt{
	private:
	int *dat, lent;
	public:
	fwt(int len){
		dat = new int[lent = len]();
	}
	void add(int pos, int val){
		//cout<< "add" << pos << "," << val << endl;
		for(;pos<lent;pos+=(pos&-pos)) dat[pos] += val;
	}
	int ask(int pos){
		for(int sum=0; 1; pos-=(pos&-pos))
			if(pos) sum += dat[pos];
			else return sum;
		return 0;
	}
	int kth(int rank){
		int pos =0;
		for(int k = (1<<19); k; k>>=1)
			if(pos + k < lent and ask(pos + k) < rank) 
				pos += k;
		return pos+1;
	}
};
class query{
	public:
	int l, r, w, id, ans;
	void in(int ii){cin>> l >> r >> w, id = ii;}
};
vector<query> qs;
vector<int> tobig;
#define CMP [&](query X,query Y)
int main(){
	ios::sync_with_stdio(0),
	cin.tie(0), cout.tie(0);
	// auto tree0=fwt(30);
	// tree0.add(5, 20),
	// tree0.add(6, 20),
	// cout << tree0.ask(7),
	// cout << tree0.kth(21);
	//return 0;
	cin >> n >> m, qs.resize(m),
	tobig.push_back(0);
	for(int i = 1; i <= n; i++)
		cin >> a[i], tobig.push_back(a[i]);
	sort(tobig.begin(), tobig.end());
	for(int i = 1; i <= n; i++)
		tosmall[tobig[i]] = i;
	fwt tree(n+2);
	for(auto&qi:qs) qi.in(++o);
	sort(qs.begin(), qs.end(), CMP{return X.l<Y.l;});
	for(auto&qi:qs) {
		while(cu < qi.l) tree.add(tosmall[a[cu++]], -1);
		while(cv < qi.r) tree.add(tosmall[a[++cv]], 1);
		qi.ans = tree.kth(qi.w);
		//cout <<"que" << qi.w <<"?" << tree.ask(3)<< endl;
	}
	sort(qs.begin(), qs.end(), CMP{return X.id<Y.id;});
	for(auto&qi:qs) cout<<tobig[qi.ans] <<endl;
}