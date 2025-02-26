#include<iostream>
#include<algorithm>
#include<vector>
#include<numeric>
#include<tuple>
#include"utils.h"
using namespace std;
const int _= 2.05e5;
typedef pair<int, int> pii;

typedef tuple<int, int, int> edge;
#define fr(x) get<0>(x)
#define to(x) get<1>(x)
#define id(x) get<2>(x)

class fwt{
	vector<int> r;
	fwt(int size){
		r.resize(size + 1);
	}
	void change(int pos, int val){
		for(; pos < r.size(); pos += (pos & -pos)){
			r[pos] = max(r[pos], val);
		}
	}
	int get(int pos){
		for(int ans = -1; ; pos -= (pos & -pos)){
			
		}
	}

};

int n, m, u, v, maxreq;
int d[_], o[_], haso[_], hasoc;
vector<int> q, e[_];
vector<edge > ee;
void tsort(){
	for(int i = 1; i <= n; i++)
		if(d[i] == 0) q.push_back(i);
	for(int i = 0; i < n; i++)
		for(int to : e[q[i]]) 
			if(--d[to] == 0) q.push_back(to);
	for(int i = 0; i < n; i++)
		o[q[i]] = i+1;
}
bool cmp(edge eu, edge ev){
	if(o[to(eu)] != o[to(ev)]) return o[to(eu)] < o[to(ev)];
	else return id(eu) < id(ev);
	// avoid eu == ev
}
vector<int> solve(vector<edge> es){
	vector<int> ans(n);
	int maxreq = 0;
	for(auto ei : es){
		if(!haso[fr(ei)])
			haso[fr(ei)] = 1, hasoc ++;
	}
}
int main(){
	ios::sync_with_stdio(0),
	cin.tie(0), cout.tie(0);
	
	cin >> n >> m;
	for(int i = 1; i <= m; i++)
		cin >> u >> v, e[u].push_back(v), ++d[v],
		ee.push_back(make_tuple(u, v, i));
	testvec(ee);
	tsort(), sort(ee.begin(), ee.end(), cmp);
	//testvec(ee);
	//for(int i = 1; i <= n; i++)
	//	cout << o[i] << " \n"[i==n];
}