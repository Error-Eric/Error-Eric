#include<vector>
#include<iostream>
#include<tuple>
template<typename T>
void testvec(std:: vector<T> &vx, std::string addinfo = "Vector"){
    std:: cout << addinfo << "["<< vx.size() << "]";
    for(int i = 0; i < vx.size() && i < 20; i++){
        std:: cout << vx[i] << ",";
    }
    std:: cout << std::endl;
}

template<typename T1, typename T2, typename T3>
std::ostream& operator<<(std::ostream& ostr, const std::tuple<T1, T2, T3>& tx){
    ostr << "(" << std::get<0>(tx) << "," << std::get<1>(tx) << ","<< std::get<2>(tx) << ")";
    return ostr;
}

void ti(std::string info){
    std::cerr << info << std::endl;
}

/*

Checklist

[LCA] If U is direct father of V? What about 1?
[SORT] If f(u) == f(v), you gotta compare u and v themselves.
[SET/MULTISET] i. sort issue. ii. delete by value == delete all;
*/