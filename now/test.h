#include<iostream>
#include<cstdio>
#include<vector>

namespace testing{
    std::string funfun(int x){
        if(x<=-1e9) return "-inf";
        else if (x>=1e9) return "inf";
        else return "";
    }
    void test(std::vector<int>&vx, std::string name = "vector"){
        std:: cout << name << "[" << vx.size() << "]:"; 
        for(unsigned int i = 0; i < 10 && i < vx.size(); i++)
            std::cout << vx[i] << ",";
        if(vx.size()>10) std::cout <<"...\n";
        else  std::cout<<"##\n";
    }
}