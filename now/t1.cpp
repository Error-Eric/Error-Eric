#include<iostream>
#include<algorithm>
#include<stdio.h>
#include<vector>
#include<numeric>
#include<map>
using namespace std;
const int _= 8.1e5;
const int M = 5.01e5;
//#define int long long
typedef long long ll;
#define LS (tree[o].ls)
#define RS (tree[o].rs)
int m, op;
ll n = 1;
struct node{
	int ls, rs, fa;
	ll lp, rp, max, tag;
}tree[_];
int countnode = 1;
void pushup(int o){
	pushdown(LS), pushdown(RS), 
	tree[o].max = max(tree[LS].max, tree[RS].max);
}
void pushdown(int o){
	tree[o].max += tree[o].tag;
	if(LS >0) tree[LS].tag += tree[o].tag;
	if(RS >0) tree[RS].tag += tree[o].tag;
	tree[o].tag = 0;
}
bool sonfy(int o){
	if(LS > 0 && RS > 0) return 0;
	else LS = ++ countnode, RS = ++ countnode;
}
void add(int o, ll ql, ll qr, ll val){
	if(ql <= tree[o].lp && tree[o].rp <= qr)
		tree[o].tag += val, pushdown(o);
	else if (ql > tree[o].rp || qr < tree[o].lp)
		return;
	//else add();
}

ll u[M], v[M], w[M];
vector<ll> specs;
//vector<ll> deps;
map<ll, ll> dep;
signed main(){
	ios::sync_with_stdio(0),
	cin.tie(0), cout.tie(0);
	cin >> m;
	for(int i = 1; i <= m; i++){
		cin>> op;
		if(op == 1) // v length w number
			cin >> u[i] >> v[i] >> w[i], specs.push_back(u[i]);
		else if(op == 2)
			cin >> u[i], u[i] = - u[i], specs.push_back(-u[i]);
		else v[i] = -2;
	}
	sort(specs.begin(), specs.end()), reverse(specs.begin(), specs.end());
	for(int i = 1; i <= m; i++){
		if(u[i] >= 0 && v[i] >= 0){
			while(n <= specs.back() && specs.back() <= n + v[i] * w[i]){
				dep[specs.back()] = dep.at(u[i]) + (specs.back() - n - 1) % v[i] + 1;
			}
		}
	}
}