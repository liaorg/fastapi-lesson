# 基础知识

## 字符串
1. 原始字符串 `r''`： print(r'\n') \n 不会转义，输出 \n
2. 字符串拼接：普通拼接：`'string' + 'string'`, 有变量的拼接：`f'{a} {b}'`, 需要重复字符串时：`'string' * n`

## 整数
1. 浮点数精度问题：使用 decimal 库来计算 `decimal.Decimal('0.1') + decimal.Decimal('0.2')`
2. 科学计数法：`0.00005 -> 5e-05` 5的负5次方
3. 复数 `x=1+2j` 1为实部x.real，2j为虚部x.imag
4. 运算符，向下取整`//`:取比目标结果小的最大整数，取余`%`: divmod(x, y) == x // y, x % y; 幂运算`**`: x**y == pow(x, y[, %n])
5. int(), float(), complex(real, imag), c.conjugate()共轭复数
6.  True, False(False, 0, 0.0, 0j, Decimal(0), Fraction(0,1),'',(),[],{},range(0), None)

### 运算符优先级
1. 括号优先级最高，括号内优先级最高，括号外优先级最低
2. await x, (+x, -x, ~x), (* @ / // %), (+ -), (<< >>), &, ^, |, 比较运算(in, not in, is, is not, <, <=, >, >=, !=, ==), not x, and, or, 条件表达式if--else，lambda 表达式，赋值表达式:= 

## 分支 条件语句
```python
if condition:
    do something
elif condition1:
    do something1
else:
    do something3

true_expression if condition else false_expression
```

## 循环语句
```python
# 当 condition 为 True 时，循环执行 do something
# break 用于跳出循环
while condition:
    do something
    break
```

## 函数
1. 关键字参数: 带有标识符或前面带有 ** 的字典里的值 `func(arg1=1, arg2=2)` `func(**{'real': 3, 'imag': 5})` 
2. 位置参数: 不属于关键字的参数  `func(arg1, arg2, ...)` `func(*(3, 5))`
3. 仅限关键字参数： 在 `*,` 之后的形参 `def func(arg, *, kw_only1, kw_only2): ...`
4. 仅限位置参数： 在 `/,` 之前的形参 ，`def func(posonly1, posonly2, /, positional_or_keyword): ...`
5. 可变位置args/可变关键字kwargs: `def func(*args, **kwargs): ...`

## lambda 表达式
1. 有时称为 lambda 构型, 被用于创建匿名函数
2. 语法：`lambda [arg1 [,arg2, ...]]: expression`