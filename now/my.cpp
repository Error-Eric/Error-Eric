#include<iostream>
#include<algorithm>
#include<vector>
#include<numeric>
#include<map>
#include<queue>
#include<unordered_set>
//#include<ranges>
using namespace std;
int q, x, y, z;
#define LS (o<<1)
#define RS (o<<1|1)
class segt{
	private:
	vector<int> dat, tree;
	map<int, queue<int> > nex;
	int lent = 2e5+5;
	segt(){
		dat.resize(lent + 5),
		tree.resize((lent << 1) + 15),
		fill(dat.begin(), dat.end(), 2.1e6),
		iota(tree.begin(), tree.end(), 0);
	}
	void chg(int o, int sl, int sr, int&qo, int&v){
		if(sl == qo && sr == qo) return (void)(dat[o] = v);
		else if(qo < sl || sr < qo) return ;
		else {
			int mid = ((sl + sr) >> 1);
			if(qo < mid) chg(LS, sl, mid, qo, v);
			else chg(RS, mid+1, sr, qo, v);
			tree[o] = (dat[tree[LS]]< dat[tree[RS]])? tree[LS] : tree[RS];
		}
	}
	int query(int o, int sl, int sr, int ql, int qr){
		if(ql <= sl && sr <= qr)return dat[o];
		else if(qr < sl || sr < ql) return lent;
		else {
			int mid = ((sl + sr) >> 1), 
			al = query(LS, sl, mid, ql, qr),
			ar = query(RS, mid+1, sr, ql, qr);
			return (dat[al] < dat[ar]) ? al : ar; 
		}
	}
	public:
	int query(int ql, int qr){return query(1, 1, lent, ql, qr);}
	void modify(int pos, int val){
		if(dat[pos]<2.05e6) nex[pos].push(val);
		else chg(1, 1, lent, pos, val);
	}
	pair<int, int> leave(int maxppl){
		int id = query(1, 1, lent, 0, maxppl), ppl = dat[id];
		if(nex.count(ppl)){
			int nexin = nex[ppl].front();
			nex[ppl].pop();
			if(nex[ppl].empty()) nex.erase(ppl); 
			chg(1, 1, lent, ppl, nexin);
		}
		else chg(1, 1, lent, ppl, lent);
		return {id, ppl};
	}
}t;

struct divgoup{
	mutable int pop;
	int id;
};
queue<divgoup> q2;
unordered_set<int> lefta;

int main(){
	ios::sync_with_stdio(0),
	cin.tie(0), cout.tie(0);
	t.modify(1, 4);
	t.modify(1, 5);
	t.modify(7, 8);
	t.modify(2, 10);

	return 0;
	cin>> q;
	while(q--){
		cin >> x;
		switch (x)
		{
		case 1: 
			cin >> x >> y,(y == 1)? 
			q2.push({x, ++z}): t.modify(x, ++z);
			cout<<"1!" << endl;
			break;
		case 2: 
			cin >> x;
			while(x){
				while(lefta.count(q2.front().id)) q2.pop();
				while(lefta.count(t.query(1, x))) t.leave(x);
				int best = t.query(1, x);
				if(q2.empty() || best < q2.front().id) 
					x -= t.leave(x).second;
				else {
					if(best > 2e5) break;
					cout << q2.front().id << " " << min(x, q2.front().pop)<< endl;
					if(x < q2.front().pop) q2.front().pop -= x, x = 0;
					else x -= q2.front().pop, q2.pop();
				}
			}
			break;
			
		default:
			cin>> x;
			lefta.insert(x);
			break;
		}
	}
}