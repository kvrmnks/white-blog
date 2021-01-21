
<!--more-->
![](file://C:/Users/Kvrmnks/Documents/Gridea/post-images/1590903931832.png)
先咕掉题解, 只贴代码吧

```cpp
#include<bits/stdc++.h>
using namespace std;
const int MOD = 1000000007;
const int MAXN = 1000005;
typedef long long ll;
int n,data[MAXN],inv[MAXN],fac[MAXN],ifac[MAXN];
int sum,qsum;
int comb(int n,int m){
    return (((ll)fac[n]*(ll)ifac[m])%MOD*(ll)ifac[n-m])%MOD;
}
int main(){
    scanf("%d",&n);
    for(int i=1;i<=n;i++)scanf("%d",data+i);
    inv[0]=inv[1]=fac[0]=ifac[0]=fac[1]=ifac[1]=1;
    for(int i=1;i<=n;i++){
        sum = (sum+data[i])%MOD;
        qsum = (qsum + ((ll)data[i]*(ll)data[i])%MOD)%MOD;
    }
    for(int i=2;i<=n+1;i++){
        inv[i]=((ll)(MOD-MOD/i)*inv[MOD%i])%MOD;
        fac[i] = ((ll)fac[i-1]*(ll)i)%MOD;
        ifac[i] = ((ll)ifac[i-1] * (ll)inv[i])%MOD;
    }
    int ans=0;
    for(int i=0;i<n;i++){ans=(ans+((ll)comb(n-1,i)*(ll)inv[i+1])%MOD)%MOD;}
    ans=((ll)ans*(ll)qsum)%MOD;
    for(int i=1;i<=n;i++){
        ll tmp = 0;
        tmp = (comb(n-1,i-1) * (ll)qsum)%MOD;
        if(i>=2)
            tmp =(tmp + ((ll)comb(n-2,i-2)*(ll)((((ll)sum*(ll)sum)%MOD-qsum)%MOD+MOD)%MOD)%MOD)%MOD;
        tmp = (tmp * (ll)(inv[i]))%MOD;
        tmp = (tmp * (ll)(inv[i]))%MOD;
        ans = (ans - tmp)%MOD;
        ans = (ans + MOD)%MOD;
    }
    printf("%d",ans);
    return 0;
}

```