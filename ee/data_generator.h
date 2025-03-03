#include<vector>
#include<random>
#include<numeric> // iota
#include<time.h>
#include<tuple>
//#include<algorithm> // shuffle

using std::vector, std::tuple, std::mt19937_64, std::make_tuple;
typedef tuple<int, int, int> t3i;

class fenwick_tree{
    vector<int>*dat = nullptr;
    fenwick_tree(int len){
        dat = new std::vector<int>(len);
    }
};

vector<t3i> generate(int num_sets, int num_merge, int num_remove_if, int rand_seed){
    vector<t3i> ret = {};
    mt19937_64 rd = mt19937_64(rand_seed);
    for(int rcm = num_merge, rcr = num_remove_if; rcm + rcr > 0; ){
        if(rd() % (rcm + rcr) < rcm) 
            ret.push_back(make_tuple(1, rd() % num_sets, rd() % num_sets));
        else 
            ret.push_back(make_tuple(2, rd() % num_sets, 0));
    }

    //return 0;
    //std::vector<int> fa = std::vector<int>(num_sets);
    //iota(fa.begin(), fa.end(), 1);
}

vector<t3i> generate(int num_sets, int num_merge, int num_remove_if){
    return(generate(num_sets, num_merge, num_remove_if, time(NULL)));
}