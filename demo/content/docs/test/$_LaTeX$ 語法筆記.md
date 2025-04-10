---
title: $\LaTeX$ 語法筆記
tags: [LaTeX]

---

> HackMD 是透過 MathJax 支援 {{< katex >}}\LaTeX{{< /katex >}} ，雖未支援所有語法，對多數人應已足夠，一起把 Web 上醜死的公式換成美美的吧～

# {{< katex >}}\LaTeX{{< /katex >}} 語法筆記

{{< katex display=true >}}

\LaTeX % 大小寫須正確

{{< /katex >}}

```
\LaTeX % 大小寫須正確

{{< katex >}}\textstyle{{< /katex >}}
{{< katex display=true >}}
\displaystyle
{{< /katex >}}
%comment
```

{{< katex display=true >}}

\grave apple % 標重音

{{< /katex >}}

```
\grave apple % 標重音
```


{{< katex display=true >}}

{\bf AB} % 粗體 boldface

{{< /katex >}}

```
{\bf AB} % 粗體 boldface
```

{{< katex display=true >}}

\bar{A}

{{< /katex >}}

```
\bar{A}
```

{{< katex display=true >}}

{ a+b \brace c+d }

{{< /katex >}}

```
{ a+b \brace c+d }
```

{{< katex display=true >}}

\overline{AB}

{{< /katex >}}

```
\overline{AB}
```

{{< katex display=true >}}

\vec{v}

{{< /katex >}}

```
\vec{v}
```

{{< katex display=true >}}

\frac{b}{a}

{{< /katex >}}

```
\frac{b}{a}
% 或
{b \over a}
```

{{< katex display=true >}}

\dfrac{b}{a}

{{< /katex >}}

```
\dfrac{b}{a}  % d for \displaystyle
\tfrac{b}{a}  % t for \textstyle
```

{{< katex display=true >}}

90^\circ

{{< /katex >}}

```
90^\circ
```

{{< katex display=true >}}

e^{\theta i}

{{< /katex >}}

```
e^{\theta i}
```

{{< katex display=true >}}

S_{n}

{{< /katex >}}

```
S_{n}
```

{{< katex display=true >}}

\lim\limits_{n\to \infty}

{{< /katex >}}

```
\lim\limits_{n\to \infty}
```

{{< katex display=true >}}

\sum\limits_{x = 0}^k{x^2}

{{< /katex >}}

```
\sum\limits_{x = 0}^k{x^2}
```

{{< katex display=true >}}

\bigcup\limits_{i = 1}^{\infty}{U_i}

{{< /katex >}}

```
\bigcup\limits_{i = 1}^{\infty}{U_i}
```

{{< katex display=true >}}

\bigcap\limits_{i = 1}^{\infty}{U_i}

{{< /katex >}}

```
\bigcap\limits_{i = 1}^{\infty}{U_i}
```

{{< katex display=true >}}

\mathop{\vcenter{\huge\times}}_\limits{i=1}^n{U_i}

{{< /katex >}}

```
\mathop{\vcenter{\huge\times}}_\limits{i=1}^n{U_i}
```

{{< katex display=true >}}

\int_a^b x^2  \mathrm{d} x

{{< /katex >}}

```
\int_a^b x^2  \mathrm{d} x
```

{{< katex display=true >}}

\sqrt[n]{1+x+x^2+x^3+\dots+x^n}

{{< /katex >}}

```
\sqrt[n]{1+x+x^2+x^3+\dots+x^n}
% 或
\root n \of {1+x+x^2+x^3+\dots+x^n}
```

{{< katex display=true >}}

A \implies B

{{< /katex >}}

```
A \implies B
```

{{< katex display=true >}}

A \impliedby B

{{< /katex >}}

```
A \impliedby B
```

{{< katex display=true >}}

A \iff B

{{< /katex >}}

```
A \iff B
```

{{< katex display=true >}}

f: A \to B

{{< /katex >}}

```
f: A \to B
```

{{< katex display=true >}}

A \leftarrow B 

{{< /katex >}}

```
A \leftarrow B
```

{{< katex display=true >}}

\xrightarrow{中文亦可}\ \xleftarrow{中文亦可}

{{< /katex >}}

```
\xrightarrow{中文亦可}\ \xleftarrow{中文亦可}
```

{{< katex display=true >}}

a\,\overset{?}{=}\,b

{{< /katex >}}

```
a\,\overset{?}{=}\,b
```

{{< katex display=true >}}

\forall x \in X, \exists x \in b

{{< /katex >}}

```
\forall x \in X, \exists x \in b
```

{{< katex display=true >}}

\not\in, \not\gt, \not\lt, \not=

{{< /katex >}}
```
\not\in, \not\gt, \not\lt, \not=   % 利用 \not 組合表示否定
```

{{< katex display=true >}}

a_{1}, a_{2}, \ldots, a_{n}

{{< /katex >}}

```
a_{1}, a_{2}, \ldots, a_{n}
```

{{< katex display=true >}}

a_{1} + a_{2} + \cdots + a_{n}

{{< /katex >}}

```
a_{1} + a_{2} + \cdots + a_{n}
```

{{< katex display=true >}}

\begin{pmatrix}
  a_{11} & a_{12} & \cdots & a_{1n}?
  a_{21} & a_{22} & \cdots & a_{2n}\\
  \vdots & \vdots & \ddots & \vdots\\
  a_{m1} & \cdots & \cdots & a_{mn}
\end{pmatrix}

{{< /katex >}}

```
\begin{pmatrix}
  a_{11} & a_{12} & \cdots & a_{1n}\\
  a_{21} & a_{22} & \cdots & a_{2n}\\
  \vdots & \vdots & \ddots & \vdots\\
  a_{m1} & \cdots & \cdots & a_{mn}
\end{pmatrix}

% ldots: low dots
% cdots: center dots
% ddots: diagonal dots
% vdots: vertical dots
```

{{< katex display=true >}}

\left\{
  \begin{array}{c}
    a_1x+b_1y+c_1z=d_1 \\ 
    a_2x+b_2y+c_2z=d_2 \\ 
    a_3x+b_3y+c_3z=d_3
  \end{array}
\right.

{{< /katex >}}

```
\left\{ 
  \begin{array}{c}
    a_1x+b_1y+c_1z=d_1 \\ 
    a_2x+b_2y+c_2z=d_2 \\ 
    a_3x+b_3y+c_3z=d_3
  \end{array}
\right.
```

# Operator/Relation

{{< katex >}}A\times B{{< /katex >}} = A\times B
{{< katex >}}a\cdot b{{< /katex >}} = a\cdot b
{{< katex >}}\div{{< /katex >}} = \div
{{< katex >}}\pmod n{{< /katex >}} = \pmod n
{{< katex >}}\pm{{< /katex >}} = \pm (plus and minus)
{{< katex >}}\partial{{< /katex >}} = \partial
{{< katex >}}\oplus{{< /katex >}} = \oplus
{{< katex >}}\&{{< /katex >}}= \\&
{{< katex >}}\gt{{< /katex >}} = \gt (greater than)
{{< katex >}}\lt{{< /katex >}} = \lt (less than)
{{< katex >}}\ge{{< /katex >}} = \ge (greater or equal)
{{< katex >}}\le{{< /katex >}} = \le (less or equal)
{{< katex >}}\lhd{{< /katex >}} = \lhd (normal subgroup)
{{< katex >}}\unlhd{{< /katex >}} = \unlhd 
{{< katex >}}\ne{{< /katex >}} = \ne (not equal)
{{< katex >}}\approx{{< /katex >}} = \approx (approximate to)
{{< katex >}}\sim{{< /katex >}} = \sim (similar)
{{< katex >}}\cong{{< /katex >}} = \cong (congruent)
{{< katex >}}\equiv{{< /katex >}} = \equiv (equivalent)
{{< katex >}}\ll{{< /katex >}} = \ll, much less than
{{< katex >}}\gg{{< /katex >}} = \gg, much greater than
{{< katex >}}\nless{{< /katex >}} = \nless, not less than
{{< katex >}}\ngtr{{< /katex >}} = \ngtr, not greater than
{{< katex >}}\cap{{< /katex >}} = \cap, 像帽子, intersection
{{< katex >}}\cup{{< /katex >}} = \cup, 像杯子, union
{{< katex >}}\subset{{< /katex >}} = \subset, or implied
{{< katex >}}\supset{{< /katex >}} = \superset, or implies
{{< katex >}}\subseteq{{< /katex >}} = \subseteq
{{< katex >}}\supseteq{{< /katex >}} = \supseteq
{{< katex >}}\land{{< /katex >}} = \land (logical and); \wedge (wedge product)
{{< katex >}}\lor{{< /katex >}} = \lor (logical or)

[List of Logic Symbols](https://en.wikipedia.org/wiki/List_of_logic_symbols)

# Function

{{< katex >}}\binom{a}{b}{{< /katex >}} = \binom{a}{b}

>Binomial : {{< katex >}}\frac{C!}{n!(n-k)!}, where\ (n+k) = constant{{< /katex >}}
或 \binom a b
或 { a \choose b }
\tbinom a b (t for \textstyle)
\dbinom a b (d for \displaystyle)

{{< katex >}}\cos{\theta}{{< /katex >}} = \cos{\theta}
{{< katex >}}\sin{\theta}{{< /katex >}} = \sin{\theta}
{{< katex >}}\log_{b}{x}{{< /katex >}} = \log_{b}{x}
{{< katex >}}\ln{x}{{< /katex >}} = \ln{x}
{{< katex >}}\lceil x \rceil{{< /katex >}} = \lceil x \rceil
{{< katex >}}\lfloor x \rfloor{{< /katex >}} = \lfloor x \rfloor

# Matrix

{{< katex display=true >}}

\begin{pmatrix}A\\B\end{pmatrix}

{{< /katex >}}

```
\begin{pmatrix}
  A\\B                % \\ 為 newline(換行)
\end{pmatrix}

% 或

\pmatrix{A\\B}
```

{{< katex display=true >}}

\begin{bmatrix}A\\B\end{bmatrix}

{{< /katex >}}

```
\begin{bmatrix}
  A\\B
\end{bmatrix}
```

{{< katex display=true >}}

\begin{vmatrix}A\\B\end{vmatrix}

{{< /katex >}}

```
\begin{vmatrix}
  A\\B
\end{vmatrix}
```

{{< katex display=true >}}

\begin{Vmatrix}A\\B\end{Vmatrix}

{{< /katex >}}

```
\begin{Vmatrix}
  A\\B
\end{Vmatrix}
```

{{< katex display=true >}}

\begin{bmatrix}
  a & b \\
  c & d 
\end{bmatrix}

{{< /katex >}}

```
\begin{bmatrix}
  a & b \\
  c & d 
\end{bmatrix}
```

# Greek
{{< katex >}}\alpha{{< /katex >}} = \alpha
{{< katex >}}\beta{{< /katex >}} = \beta
{{< katex >}}\Delta{{< /katex >}} = \Delta, {{< katex >}}\delta{{< /katex >}} = \delta
{{< katex >}}\epsilon{{< /katex >}} = \epsilon, {{< katex >}}\varepsilon{{< /katex >}} = \varepsilon
{{< katex >}}\gamma{{< /katex >}} = \gamma
{{< katex >}}\theta{{< /katex >}} = \theta
{{< katex >}}\sigma{{< /katex >}} = \sigma
{{< katex >}}\pi{{< /katex >}} = \pi
{{< katex >}}\mu{{< /katex >}} = \mu
{{< katex >}}\lambda{{< /katex >}} = \lambda
{{< katex >}}\omega{{< /katex >}} = \omega
{{< katex >}}\phi{{< /katex >}} = \phi
{{< katex >}}\varphi{{< /katex >}} = \varphi
{{< katex >}}\rho{{< /katex >}} = \rho

# Misc
{{< katex >}}\angle{{< /katex >}} = \angle
{{< katex >}}\triangle{{< /katex >}} = \triangle
{{< katex >}}\square{{< /katex >}} = \square
{{< katex >}}\quad (space){{< /katex >}} = \quad (space)
{{< katex >}}\propto{{< /katex >}} = \propto (propotional to)

{{< katex >}}\because{{< /katex >}} = \because
{{< katex >}}\therefore{{< /katex >}} = \therefore
{{< katex >}}\mathbb{Z}{{< /katex >}} = \mathbb{Z}
{{< katex >}}\mathbb{P}{{< /katex >}} = \mathbb{P}
{{< katex >}}\mathbb{R}{{< /katex >}} = \mathbb{R}
{{< katex >}}\mathbb{C}{{< /katex >}} = \mathbb{C}
{{< katex >}}\Im{{< /katex >}} = \Im (Imaginary Space)
{{< katex >}}\Re{{< /katex >}} = \Re (Real Space)

{{< katex >}}\emptyset{{< /katex >}} = \emptyset
{{< katex >}}\varnothing{{< /katex >}} = \varnothing (以此表示空集合較好看)
{{< katex >}}\in{{< /katex >}} = \in
{{< katex >}}\not\in{{< /katex >}} = \not\in
{{< katex >}}\langle S\rangle{{< /katex >}} = \langel S\rangle (generator)
{{< katex >}}\chi{{< /katex >}} = \chi
{{< katex >}}\circlearrowleft{{< /katex >}} = \circlearrowleft
{{< katex >}}\circlearrowright{{< /katex >}} = \circlearrowright
{{< katex >}}\curvearrowleft{{< /katex >}} = \curvearrowleft
{{< katex >}}\curvearrowright{{< /katex >}} = \curvearrowright
{{< katex >}}\hbar{{< /katex >}} = \hbar (Planck's Constant)


https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols#Set_and.2For_logic_notation

# Format

## Style

{{< katex display=true >}}

\style{background-color:#eeeeee}{\frac{x+1}{y+2}}

{{< /katex >}}

```
\style{background-color:#eeeeee}{\frac{x+1}{y+2}}  % 直接以 CSS 改變 style
```

{{< katex display=true >}}

f(x) = a{\color{red}{x}} + b

{{< /katex >}}

```
f(x) = a{\color{red}{x}} + b
% 或
f(x) = a{\color{#ff0000}{x}} + b
```

{{< katex display=true >}}

\require{color}
\colorbox{#eeeeee}{Color Box}

{{< /katex >}}

```
\require{color}
\colorbox{#eeeeee}{Color Box}
```

{{< katex display=true >}}

{\cal ABCDE12345abcde}

{{< /katex >}}

```
{\cal ABCDE12345abced} % callgraphic mode
```

{{< katex display=true >}}

\fbox{boxed text}

{{< /katex >}}

```
\fbox{boxed text}      % in textstyle
```

{{< katex display=true >}}

\boxed{boxed\ text}

{{< /katex >}}

```
\boxed{boxed\ text}    % in displaystyle
```

{{< katex display=true >}}

\text{text {{< katex >}}E=mc^2{{< /katex >}}}

{{< /katex >}}
```
\text{text {{< katex >}}E=mc^2{{< /katex >}}}
```

{{< katex display=true >}}

{\frak ABCDE12345abcde}

{{< /katex >}}

```
{\frak ABCDE12345abcde}
```

{{< katex display=true >}}

{\it abefg12345}\ abcdefg12345

{{< /katex >}}

```
{\it abefg12345}\ abcdefg12345   % italic
```
{{< katex display=true >}}

\min\limits_{n}

{{< /katex >}}
```
\min\limits_{n}
```


## Automatic Sizing

{{< katex display=true >}}

\{x \mid x\gt 1\}\text{ 與 }\{x | x\gt 1\}

{{< /katex >}}

```
\{x \mid x\gt 1\}     % 請用 \mid 寫 Set 才好看
```

{{< katex display=true >}}

\left( \dfrac{x^2}{y^3} \right)

{{< /katex >}}

```
\left(\dfrac{x^2}{y^3}\right)
```

{{< katex display=true >}}

\left\{ \dfrac{1}{2} \right\}

{{< /katex >}}

```
\left\{ \dfrac{1}{2} \right\}
```

{{< katex display=true >}}

f(x) = \left\{
\begin{array}{r} 
x + by = c \\ 
dx + ey = f 
\end{array}
\right.

{{< /katex >}}

```
f(x) = \left\{
\begin{array}{r}
   x + by = c \\
  dx + ey = f 
\end{array}
\right.

% {r} for right alignment within array
% {l} for left alignment within array
% 或

\array{
   x + by = c \\
  dx + ey = f 
}
```

{{< katex display=true >}}

z = \overbrace{
      \underbrace{x}_\text{real} + i
      \underbrace{y}_\text{imaginary}
}^\text{complex number}

{{< /katex >}}

```
z = \overbrace{
    \underbrace{x}_\text{real} + i
    \underbrace{y}_\text{imaginary}
}^\text{complex number}
```

## Alignment

{{< katex display=true >}}

\begin{aligned}
f(x) &= ax + by + cz + d \\
     &= 2x + 3y + 5z + 1
\end{aligned}

{{< /katex >}}

```
\begin{aligned}
f(x) &= ax + by + cz + d \\
     &= 2x + 3y + 5z + 1
\end{aligned}

% 或

\begin{align}
f(x) &= ax + by + cz + d \\
     &= 2x + 3y + 5z + 1
\end{align}

% 或

\eqalign{
f(x) &= ax + by + cz + d \\
     &= 2x + 3y + 5z + 1
}
```

{{< katex display=true >}}

\begin{cases}n/2, & \text{if {{< katex >}}n{{< /katex >}} is even} \\
3n+1, & \text{if {{< katex >}}n{{< /katex >}} is odd}
\end{cases}

{{< /katex >}}

```
\begin{cases}
  n/2, & \text{if {{< katex >}}n{{< /katex >}} is even} \\
  3n+1, & \text{if {{< katex >}}n{{< /katex >}} is odd}
\end{cases}

% 或

\cases{
  n/2, & \text{if {{< katex >}}n{{< /katex >}} is even} \\
  3n+1, & \text{if {{< katex >}}n{{< /katex >}} is odd}
}
```

{{< katex display=true >}}

\begin{pmatrix}
 aaa & bbb \\
 cc & dd
\end{pmatrix}

{{< /katex >}}

```
\begin{pmatrix}
 aaa & bbb \\
 cc & dd
\end{pmatrix}
```

{{< katex display=true >}}

\begin{matrix}
  xxxxxx & xxxxxx & xxxxxx \cr
  ab & \hfil ab & ab\hfil \cr
\end{matrix}

{{< /katex >}}

```
\begin{matrix}
  xxxxxx & xxxxxx & xxxxxx \cr
  ab & \hfil ab & ab\hfil \cr    % 以 \hfil 自動填空
\end{matrix}
```

{{< katex display=true >}}

\begin{array}{rrrrrr|r}
       & x_1 & x_2 & s_1 & s_2 & s_3 &    \\ \hline
   s_1 &   0 &   1 &   1 &   0 &   0 &  8 \\
   s_2 &   1 &  -1 &   0 &   1 &   0 &  4 \\
   s_3 &   1 &   1 &   0 &   0 &   1 & 12 \\ \hline
       &  -1 &  -1 &   0 &   0 &   0 &  0
\end{array}

{{< /katex >}}

```
\begin{array}{rrrrrr|r}
       & x_1 & x_2 & s_1 & s_2 & s_3 &    \\ \hline
   s_1 &   0 &   1 &   1 &   0 &   0 &  8 \\
   s_2 &   1 &  -1 &   0 &   1 &   0 &  4 \\
   s_3 &   1 &   1 &   0 &   0 &   1 & 12 \\ \hline
       &  -1 &  -1 &   0 &   0 &   0 &  0
\end{array}
```

# Advanced

{{< katex display=true >}}

\overset{上組合技}{\implies} 或\underset{下組合技}{\impliedby}

{{< /katex >}}

```
\overset{上組合技}{\implies} 或 \underset{下組合技}{\impliedby}
```

{{< katex display=true >}}

\require{extpfeil}
x\xtofrom[f^{-1}]{f} y

{{< /katex >}}

```
\require{extpfeil}
x \xtofrom[f^{-1}]{f} y
```

{{< katex display=true >}}

\require{mhchem}
x \xrightleftharpoons[f^{-1}]{f} y

{{< /katex >}}

```
\require{mhchem}
x \xrightleftharpoons[f^{-1}]{f} y
```

{{< katex display=true >}}

\require{ams}
\begin{equation}
   \tag{1}\label{eq:eq_1} E = mc^2  
\end{equation}

{{< /katex >}}

```
\require{ams}
\begin{equation}
   \tag{1}\label{eq:eq_1} E = mc^2 
\end{equation}
% MathJax 照理說已支援 Auto Number，但 HackMD 不支援。
% 只能手動自己加 \tag{1}\label{eq:equation_name}
```

{{< katex display=true >}}

reference\ equation\eqref{eq:eq_1}

{{< /katex >}}

```
reference\ equation\eqref{eq:eq_1}
```

{{< katex display=true >}}

\begin{equation*}
   E = mc^2
\end{equation*}

{{< /katex >}}

```
\begin{equation*}
  E = mc^2
\end{equation*}
% 不加入 Auto Number，但在 HackMD 上沒差別。
```

{{< katex display=true >}}

\def \kton{\sum\limits_{k=0}^{n}}
\begin{aligned}
(1+\frac{1}{n})^n &= \kton \binom{n}{k}1^{n-k}(\frac{1}{n})^{k}\\
&= \kton \binom{n}{k} \frac{1}{n^{k}}\\
&= \kton \frac{n!}{k!(n-k)!}\times\frac{1}{n^k}\\
&= \kton \frac{1}{k!} \frac{\overbrace{n(n-1)(n-2)\ldots(n-k+1)}^{共\ k\ 項}}{n^k}\\
&= \kton \frac{1}{k!} (\frac{n}{n}\frac{n-1}{n}\cdots\frac{n-k+1}{n})
\end{aligned}

{{< /katex >}}

```
% 若命令又長又重複，可用 \def 自訂

\def \kton{\sum\limits_{k=0}^{n}}
\begin{aligned}
  (1+\frac{1}{n})^n &= \kton \binom{n}{k}1^{n-k}(\frac{1}{n})^{k}\\
  &= \kton \binom{n}{k} \frac{1}{n^{k}}\\
  &= \kton \frac{n!}{k!(n-k)!}\times\frac{1}{n^k}\\
  &= \kton \frac{1}{k!} \frac{\overbrace{n(n-1)(n-2)\ldots(n-k+1)}^{共\ k\ 項}}{n^k}\\
  &= \kton \frac{1}{k!} (\frac{n}{n}\frac{n-1}{n}\cdots\frac{n-k+1}{n})
\end{aligned}
```

{{< katex display=true >}}

\DeclareMathOperator {\total}{總計}
\total_a^b(x)

{{< /katex >}}

```
\DeclareMathOperator {\total}{總計}
\total_a^b(x)
% 自訂 Operator，命名限 [a-z|A-Z]，不可含數字。
```

## 微調字體、字距

### Font

{{< katex display=true >}}

\mathbb{ABCDE12345abcde}

{{< /katex >}}

\mathbb - Used to turn on blackboard-bold for uppercase letters and lowercase 'k'.

{{< katex display=true >}}

\mathbf{ABCDE12345abcde}

{{< /katex >}}

\mathbf - Used to turn on boldface for uppercase and lowercase letters and digits.

{{< katex display=true >}}

\mathit{ABCDE12345abcde}

{{< /katex >}}

\mathit - forces the math italic mode.

{{< katex display=true >}}

\mathcal{ABCDE12345abcde}

{{< /katex >}}

\mathcal - Used to turn on calligraphic font for uppercase letters and digits.

{{< katex display=true >}}

\mathfrak{ABCDE12345abcde}

{{< /katex >}}

\mathfrak - turn on fraktur font for uppercase and lowercase letters and digits (and a few other characters).

{{< katex display=true >}}

\mathrm{ABCDE12345abcde}

{{< /katex >}}

\mathrm - Used to turn on roman typestyle for uppercase and lowercase letters.

{{< katex display=true >}}

\mathscr{ABCDE12345abcde}

{{< /katex >}}

\mathscr - Used to turn on script typestyle for uppercase letters. If lowercase script letters are not available, then they are typeset in a roman typestyle.

{{< katex display=true >}}

\mathsf{ABCDE12345abcde}

{{< /katex >}}

\mathsf - Used to turn on sans serif typestyle for uppercase and lowercase letters and digits; also affects uppercase greek.

{{< katex display=true >}}

\mathtt{ABCDE12345abcde}

{{< /katex >}}

\mathtt - Used to turn on typewriter typestyle for uppercase and lowercase letters and digits.

{{< katex display=true >}}

\oldstyle{ABCDE12345abcde}

{{< /katex >}}

\oldstyle - Used to turn on oldstyle font.

### Operator (Class Assignment)

\mathord - forces the argument to be treated in the 'ordinary' class.
\mathrel - forces the argument to be treated in the 'relation' class.
\mathinner - forces the argument to appear 'inside' other formulas, and should be surrounded by additional space in certain circumstances.
\mathbin - Used to give the correct spacing to make an object into a binary operator.
\mathstrut - Used to achieve more uniform appearance in adjacent formulas as an invisible box whose width is zero.
\mathpunct
\mathopen
\mathclose
\mathop
```
\mathxxx{argument}
```
\mathchoice - provides content that is dependent on the current style (display, text, script, or scriptscript).
```
\mathchoice{D}{T}{S}{SS}
```

# More
* https://en.wikibooks.org/wiki/LaTeX/Mathematics
* https://en.wikibooks.org/wiki/LaTeX/Advanced_Mathematics#Custom_operators
* https://en.wikibooks.org/wiki/LaTeX/Mathematics#Adding_text_to_equations
* [MathJax Tutorial](https://math.meta.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference)
* https://tex.stackexchange.com/
* [手寫辨認查詢](http://detexify.kirelabs.org/classify.html)
* [MathJax Commands](http://docs.mathjax.org/en/latest/input/tex/macros/index.html)
* [LaTeX Arrows](https://www.sascha-frank.com/Arrow/latex-arrows.html)
* https://en.wikipedia.org/wiki/List_of_logic_symbols
* [{{< katex >}}\LaTeX{{< /katex >}} for Twitch Chat](https://rintaroutw.github.io/LaTeX4TwitchChat/)

###### tags: `LaTeX`
