#include<iostream>
#include<algorithm>
#include<vector>
#include<numeric>
//#include<ranges>
using namespace std;
typedef pair<int, int> pii;
int n, c, x, tot;
vector<int> points, stk, ans, dest;
vector<pii > pairs;
#define LP pairs.back().first, pairs.back().second
int main(){
	ios::sync_with_stdio(0),
	cin.tie(0), cout.tie(0);
	cin >> n >> c;
	for(int i : {-1,1})
		for(int j = 1; j <= n; j++)
			cin >> x, points.push_back(i*x);
	sort(points.begin(), points.end(), 
		[&](int u,int v){return abs(u)<abs(v);});
	for(int px : points){
		if(stk.empty() || stk.back() * px > 0) stk.push_back(px);
		else pairs.push_back({stk.back(), px}), stk.pop_back();
	}
	sort(pairs.begin(), pairs.end(), 
		[&](pii u, pii v){return abs(u.first)> abs(v.first);});
	//for(auto px : pairs)
	//	cout << px.first << " " << px.second << endl;
	while(pairs.size()){
		dest.clear(), x= 0;
		for(int i = 1; i <= c; i++){
			if(x == 0){
				tot += abs(pairs.back().first+pairs.back().second);
			}
			if(pairs.size() && pairs.back().first * x >= 0)
				dest.push_back(max(LP)), 
				ans.push_back(min(LP)),
				x = pairs.back().first,
				pairs.pop_back();
			else break;
		}
		while(dest.size()) 
			ans.push_back(-dest.back()), dest.pop_back();

	}
	cout << tot << endl;
	for(int ax : ans) cout << -ax << " ";
}