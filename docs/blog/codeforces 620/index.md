老年人来打场div2
<!--more-->

#### A
##### 题目简介
两只兔子往中间跳,问能不能跳到一起,能输出时间

傻逼题

```cpp
#include<bits/stdc++.h>
using namespace std;
int main(){
	int t;
	scanf("%d",&t);
	for(int i=1;i<=t;i++){
		int x,y,a,b;
		scanf("%d%d%d%d",&x,&y,&a,&b);
		y-=x;
		a+=b;
		if(y%a){
			puts("-1");
		}else{
			printf("%d\n",y/a);
		}
	} 
	
	return 0;
} 
```

#### B
##### 题目大意
给一些长度一样长的字符串,问最多能构造出多长的回文串

傻逼题*2


```cpp
#include<bits/stdc++.h>
using namespace std;
const int MAXN = 105;
bool isRev[MAXN];
bool used[MAXN];
bool lk[MAXN][MAXN];
char str[MAXN][55];
int n,m;
int Q[MAXN],top;
bool isR(int x){
	bool flag = true;
	for(int i=1;i<=m;i++){
		if(str[x][i] != str[x][m-i+1]){
			flag = false;
		}
	}
	return flag;
}
bool canlk(int x,int y){
	bool falg = true;
	for(int i=1;i<=m;i++){
		if(str[x][i] != str[y][m-i+1]){
			falg = false;
			break;
		}
	}
	return falg;
}
int main(){
	scanf("%d%d",&n,&m);
	for(int i=1;i<=n;i++){
		scanf("%s",str[i]+1);
	}
	for(int i=1;i<=n;i++)
		isRev[i] = isR(i);
	for(int i=1;i<=n;i++){
		for(int j=i+1;j<=n;j++){
			lk[i][j] = lk[j][i] = canlk(i,j);
		}
	}
	int mxlen = 0;
	for(int i=1;i<=n;i++){
		for(int j=i+1;j<=n;j++){
			if(lk[i][j] && used[i]==false && used[j] == false){
				mxlen += 2*m;
				used[i] = used[j] = true;
			}
		}
	}
	int tmp = 0;
	memset(used,0,sizeof used);
	for(int i=1;i<=n;i++){
		memset(used,0,sizeof used);
		tmp = 0;
		if(isRev[i]){
			used[i] = true;
			tmp += m;
			for(int j=1;j<=n;j++){
				for(int k=j+1;k<=n;k++){
					if(lk[j][k] && used[j]==false && used[k]==false){
						tmp += m*2;
						used[j] = used[k] = true;
					}
				}
			}
			mxlen = max(mxlen,tmp);
		}
	}
	printf("%d\n",mxlen);
	tmp = 0;
	memset(used,0,sizeof used);
	for(int i=1;i<=n;i++){
		for(int j=i+1;j<=n;j++){
			if(lk[i][j] && used[i]==false && used[j] == false){
				tmp += 2*m;
				used[i] = used[j] = true;
			}
		}
	}
	if(tmp == mxlen){
		memset(used,0,sizeof used);
		for(int i=1;i<=n;i++){
			for(int j=i+1;j<=n;j++){
				if(lk[i][j] && used[i]==false && used[j] == false){
					//tmp += 2*m;
					Q[++top] = i;
					Q[++top] = j;
					used[i] = used[j] = true;
				}
			}
		}	
		for(int i=1;i<=top;i+=2){
			printf("%s",str[Q[i]]+1);
		}
		for(int i=top;i>=1;i-=2){
			printf("%s",str[Q[i]]+1);
		}
		return 0;
	}
	for(int i=1;i<=n;i++){
		memset(used,0,sizeof used);
		tmp = 0;
		if(isRev[i]){
			used[i] = true;
			tmp += m;
			for(int j=1;j<=n;j++){
				for(int k=j+1;k<=n;k++){
					if(lk[j][k] && used[j]==false && used[k]==false){
						tmp += m*2;
						used[j] = used[k] = true;
					}
				}
			}
			//mxlen = max(mxlen,tmp);
		}
		if(tmp == mxlen){
			memset(used,0,sizeof used);
			Q[0] = i;
			used[i] = true;
			for(int j=1;j<=n;j++){
				for(int k=j+1;k<=n;k++){
					if(lk[j][k] && used[j]==false && used[k]==false){
						//tmp += m*2;
						Q[++top] = j;
						Q[++top] = k;
						used[j] = used[k] = true;
					}
				}
			}
			for(int i=1;i<=top;i+=2){
				printf("%s",str[Q[i]]+1);
			}
			printf("%s",str[Q[0]]+1);
			for(int i=top;i>=1;i-=2){
				printf("%s",str[Q[i]]+1);
			}	
			return 0;		
		}
	}
	return 0;
}
```

#### C
##### 题目大意

在一个数轴上,给定起点,1s只能走一个单位长度,给n个区间,问能不能,在相应的时间属于相应的区间

数据范围差评,好久没打cf了,总是想找个1e7+的复杂度...

直接每步维护一个区间

xjb求交就行了

```cpp
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAXN = 120;
ll t[MAXN],l[MAXN],r[MAXN];
int n;
ll L,R;
void solve(){
	scanf("%d%lld",&n,&L);
	R = L;
	for(int i=1;i<=n;i++){
		scanf("%lld%lld%lld",&t[i],&l[i],&r[i]);
	}
	for(int i=1;i<=n;i++){
		L -= t[i] - t[i-1];
		R += t[i] - t[i-1];
		if(L>r[i] || R < l[i]){
			puts("NO");
			return;
		}else{
			L = max(L,l[i]);
			R = min(R,r[i]);
		}
	}
	puts("YES");
}
int main(){
	int Q;
	scanf("%d",&Q);
	while(Q--){
		solve();
	}
	return 0;
} 
```

#### D
##### 题目大意

给一个大于小于号的序列,构造两个数列,每个数>=1,<=n,要求一个LIS最大,一个LIS最小

heheda,比赛的时候看错题了

考虑求LIS的nlogn做法,实际上我们只需要在二分的那一步改成贪心,用贪心维护那个上升数列就好了

构造的时候我是先把数分层,然后每层构造,有些小细节见代码

```cpp
#include<bits/stdc++.h>
using namespace std;
const int MAXN = 200050;
int Q,n;
char str[MAXN];
int type[MAXN],raw[MAXN];
vector<int> V[MAXN];
int Min;
void cons(int x,int pre){
	if(raw[x]!=0)return;
	
	if(x+1 <= n && type[x+1] == type[x] && pre != x+1 && str[x] == '>'){
		cons(x+1,x);
		raw[x] = raw[x+1] + 1;
	}
	if(x-1 >= 1 && type[x-1] == type[x] && pre != x-1 && str[x-1] == '<'){
		cons(x-1,x);
		raw[x] = raw[x-1] + 1;
	}
	raw[x] = Min + 1;
	Min ++;
}
void Cons(int x,int pre){
	if(raw[x]!=0)return;
	if(x-1 >= 1 && type[x-1] == type[x] && pre != x-1 && str[x-1] == '<'){
		cons(x-1,x);
		raw[x] = raw[x-1] + 1;
	}	
	if(x+1 <= n && type[x+1] == type[x] && pre != x+1 && str[x] == '>'){
		cons(x+1,x);
		raw[x] = raw[x+1] + 1;
	}

	raw[x] = Min + 1;
	Min ++;
}
void solve(){
	scanf("%d",&n);
	scanf("%s",str+1);
	int lastpos = 1;
	int mx = 1;
	type[1] = 1;

	for(int i=1;i<n;i++){
		if(str[i] == '>'){
			lastpos = 1;
			type[i+1] = 1;
		}else{
			lastpos++;
			mx = max(mx,lastpos);
			type[i+1] = lastpos;
		}
	}
	for(int i=1;i<=n;i++){
		V[type[i]].push_back(i);
	}
	Min = 0;
	for(int i=1;i<=n;i++){
		for(int j=(int)V[i].size()-1;j>=0;j--){
			cons(V[i][j],V[i][j]);
		}
	}
	for(int i=1;i<=n;i++){
		printf("%d ",raw[i]);
	}
	puts("");		
	
		
	
	for(int i=1;i<=n;i++)
		V[i] = vector<int>();
	for(int i=1;i<=n;i++)
		raw[i] = 0;
		
	lastpos = 1;
	mx = 1;
	type[1] = 1;
	
	for(int i=1;i<n;i++){
		if(str[i] == '>'){
			lastpos = 1;
			type[i+1] = 1;
		}else{
			++mx;
			lastpos = mx;
			type[i+1] = lastpos;
		}
	}
	for(int i=1;i<=n;i++){
		V[type[i]].push_back(i);
	}
	Min = 0;
	for(int i=1;i<=n;i++){
		for(int j=0;j<(int)V[i].size();j++){
			Cons(V[i][j],V[i][j]);
		}
	}
	for(int i=1;i<=n;i++){
		printf("%d ",raw[i]);
	}
	puts("");
	
	
	for(int i=1;i<=n;i++)
		V[i] = vector<int>();
	for(int i=1;i<=n;i++)
		raw[i] = 0;
}
int main(){
	scanf("%d",&Q);
	while(Q--){
		solve();
	}
	return 0;
}
```

其实原题不需要构造的答案是个排列

~~我只是不会写不是排列的做法~~

#### E
##### 题目大意

给一棵树,每次询问加一条边(x,y),询问是否有从a到b有长度等于k的可重边路径,该次询问完删掉(x,y)边

一共就3种可能 

1.a -> b

2.a -> x -> y -> b

3.a -> y -> x -> b

然后只要满足小于k且奇偶性一样就行

好久没写树链剖分了,写得头疼...

```cpp
#include<bits/stdc++.h>
using namespace std;
const int MAXN = 200050;
int sz[MAXN],top[MAXN],dep[MAXN],to[MAXN],nx[MAXN],h[MAXN],tot;
int ch[MAXN],fa[MAXN];
int n;
void add_edge(int x,int y){
	to[++tot] = y;
	nx[tot] = h[x];
	h[x] = tot;
}
void link(int x,int y){
	add_edge(x,y);
	add_edge(y,x);
}
void dfs1(int x,int y){
	sz[x] = 1;
	fa[x] = y;
	dep[x] = dep[y] + 1;
	for(int i=h[x];i;i=nx[i]){
		if(to[i] == y)
			continue;
		dfs1(to[i],x);
		sz[x] += sz[to[i]];
		if(sz[to[i]] > sz[ch[x]])
			ch[x] = to[i];
	}
}
int lca(int x,int y){
	while(top[x]!=top[y]){
		dep[top[x]] > dep[top[y]] ? x = fa[top[x]] : y = fa[top[y]];
	}
	return dep[x]<dep[y]?x:y;
}
int dis(int x,int y){
	return dep[x] + dep[y] - 2 * dep[lca(x,y)];
}
void dfs2(int x,int tp){
	top[x] = tp;
	if(ch[x])dfs2(ch[x],tp);
	for(int i=h[x];i;i=nx[i]){
		if(to[i] == fa[x] || to[i] == ch[x])
			continue;
		dfs2(to[i],to[i]);
	}
}
int main(){
	scanf("%d",&n);
	for(int i=1;i<n;i++){
		int x,y;
		scanf("%d%d",&x,&y);
		link(x,y);
	}
	dfs1(1,0);
	dfs2(1,1);
	int Q,x,y,a,b,k;
	scanf("%d",&Q);
	while(Q--){
		scanf("%d%d%d%d%d",&a,&b,&x,&y,&k);
	//	cout<<lca(x,y)<<endl;
		int tmp = dis(x,y);
		if(tmp <= k && ((k-tmp)%2==0)){puts("YES");continue;}
		tmp = dis(x,a)+dis(y,b)+1;
		if(tmp <= k && ((k-tmp)%2==0)){puts("YES");continue;}
		tmp = dis(x,b) + dis(y,a) + 1;
		if(tmp <= k && ((k-tmp)%2==0)){puts("YES");continue;}
		puts("NO");
	}
	return 0;
} 
```

#### F
##### 简单口胡
老年人不想写线段树了...

咕咕咕
