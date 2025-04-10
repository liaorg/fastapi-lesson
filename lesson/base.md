# 基础知识
> [Python 语言参考手册](https://docs.python.org/zh-cn/3.12/index.html)
[《零基础入门学习Python》最新版](https://www.bilibili.com/video/BV1c4411e77t?spm_id_from=333.788.videopod.episodes)

## 字符串
1. 原始字符串 `r''`： print(r'\n') \n 不会转义，输出 \n
2. 字符串拼接：普通拼接：`'string' + 'string'`, 有变量的拼接：`f'{a} {b}'`, 需要重复(*拷贝引用)字符串时：`'string' * n`\
    `str.join(iterable)`
3. print() 默认打印换行，结尾不换行：`print('string', end='')`
4. 大小写转换：`str.lower()` 更强大的转换小写`str.casefold()` `str.upper()` 首字母大写其他字母小写`str.title()` \
   首字母大写`str.capitalize()` 字母翻转`str.swapcase()`
5. 左中右对齐：`str.ljust(width, fillchar='')` `str.rjust(width, fillchar='')` 居中：`str.center(width, fillchar='')` 用0填空左侧`zfill(width)`
6. 查找：`str.find(sub, start, end)` `str.rfind(sub, start, end)` `str.index(sub, start, end)`\
   `str.rindex(sub, start, end)` `str.count(sub[, start[, end]] )` 
7. 替换： 空格替换制表符并返回新字符串`str.expandtabs([tabsize=4])` `str.replace(old, new[, max=-1])` \
   分割字符串`str.split(sep=None, maxsplit=-1)` `str.rsplit(sep=None, maxsplit=-1)` \
   以换行符分割字符串`str.splitlines()`
   以sep分割字符串`str.partition(sep)` `str.rpartition(sep)` \
   去除左右空白/chart`str.strip([chars])` `str.lstrip([chars])` `str.rstrip([chars])` \
   返回根据table参数返回的新字符串`str.translate(table)` table用`str.maketrans(x[, y[, z]])`生成
8. 判断：`str.isprintable()` `str.isascii()` `str.isupper()` `str.islower()` \
   是否都是字母`str.isalpha()`  都是大写开头`str.istitle()` `str.isspace()` \
   是否出现在起始位置,prefix可以为一个元组`str.startswith(prefix[, start[, end]])` `str.endswith(suffix[, start[, end]])` \ 
   `str.isdigit()` `str.isdecimal()` `str.isnumeric()` `str.isalnum()` 是否合法标志符`str.isidentifier()` `keyword.iskeyword(name)`
9. 格式化字符串 `str.format(value[, format_spec])`: `"1+2={}，2的平方={1}, 3的平方={three}".format(1+2, 2**2,tree=9)` f字符串：`f"文本{表达式:格式说明符}更多文本"` 
10. f字符串格式说明符：
### f字符串格式说明符

| 类别   | 格式说明符| 作用  |
|--------|------------------|----------------------------------------------------------------------|
| 对齐   | `:<n`, `:>n`, `:^n` | 左/右/居中对齐 |
| 填充   | `:填充字符<宽度` | 自定义填充字符，用于在对齐时填充空白区域 |
| 浮点数 | `:.nf`, `:.n%`, `:.ne`, `:.nE`, `:,` | 小数位数、百分比、科学计数法、千位分隔符 |
| 整数   | `:b`, `:o`, `:x`, `:X` | 进制、八进制、十六进制小写、十六进制大写 |
| 符号   | `:+`, `:-`, `: ` | 强制显示正负号、正数前加空格|
| 类型转换 | `!s`, `!r`, `!a` | str(), repr(), ascii() |
| 日期   | `%Y-%m-%d %H:%M:%S` | 格式化日期时间，`f"{now:%Y-%m-%d %H:%M:%S}"  # '2024-03-15 14:30:00'` |

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
# break 跳出整个循环，只跳转一层循环体
# continue 跳出本次循环
while condition:
    do something
    break

while condition:
    do something
else:
    do something

# iterable 为可迭代的对象
# 多用于访问序列的元素
for [index, ]item in iterable:
    do something
```

## 列表(可变)
1. 创建list： `[]` 嵌套列表，矩阵 `[[],[]]`
2. 索引： `list[index]` `list[len(list) -1]` `list[-1]` \
   切片：`list[:]` `list[start:]` `list[:end]` `list[start:end]` `list[start:end:step]` \
   按步进切片：`list[::step]`，step 为负数时逆序输出
   拼接：`*` `+`
3. 删除： `del list[index]` `list.pop(index)` `list.remove(item)` `list.clear()`
4. 添加：一个`list.append(item)` `list[len(list):] = [n]` 多个`list.extend(iterable)` `list[len(list):] = [n,n2,n3]` 任意位置`list.insert(index, item)`
5. 替换: `list[index] = item` `list[start:end] = [n,n2,n3]`
6. 排序: `list.sort(key, reverse)` `list.sort()` `list.sort(key=lambda x: x[0])` 不会改变源的排序`sorted(iterable)` `sorted(iterable, key=lambda x: x[0])`，
7. 倒序：`list.sort(reverse=True)`
8. 反转：`list.reverse()` `list[::-1]` `reversed(seq)`
9. 查询：`list.index(item, start, end)` `list.count(item)` `list.find(item)` `list.find(item, start, end)` `list.find(item, start)`
10. 潜拷贝：`list.copy()` `list[:]`
11. 深拷贝：
```python
import copy
copy.copy(list)
copy.deepcopy(list)
```
12. 列表推导式：`[expression for item in iterable]` `[expression for item in iterable if condition]` `[expression for item in iterable if condition1 and condition2]` `[expression for item1 in iterable1 for item2 in iterable2]` `[expression1 if condition else expression2 for item in iterable]` `[[expression for item in inner_iterable] for item in outer_iterable]`，顺序：for 语句-》if 语句 -》expression 条件
```python
oho = [1,2,3,4,5]
oho_square = [x**2 for x in oho] # [1, 4, 9, 16, 25]

# 嵌套列表
r = [[x] * 3 for x in range(3)]
# 展开
r = [item for sublist in r for item in sublist]
```
13. 打包和解包：`a,b,c = [1,2,3]`

## 元组(不可变)
1. 创建tuple：`()` `(1,2,3)` `(1,)` `1,2,3`
2. 切片同列表
3. 打包和解包：`a,b,c=(1,2,3)`  `a,*b=(1,2,3)`*表示剩余的元素赋值给b

## 函数
1. 关键字参数: 带有标识符或前面带有 ** 的字典里的值 `func(arg1=1, arg2=2)` `func(**{'real': 3, 'imag': 5})` 
2. 位置参数: 不属于关键字的参数  `func(arg1, arg2, ...)` `func(*(3, 5))`
3. 仅限关键字参数： 在 `*,` 之后的形参 `def func(arg, *, kw_only1, kw_only2): ...`
4. 仅限位置参数： 在 `/,` 之前的形参 ，`def func(posonly1, posonly2, /, positional_or_keyword): ...`
5. 可变位置args/可变关键字kwargs: `def func(*args, **kwargs): ...`

## lambda 表达式
1. 有时称为 lambda 构型, 被用于创建匿名函数
2. 语法：`lambda [arg1 [,arg2, ...]]: expression`

## 迭代器 vs 可迭代对象
1. 可迭代对象： 可重复使用
2. 迭代器：`iter(iterable)` 只能使用一次，`next(iterator[, default])`每次迭代都会返回下一个元素，直到没有元素为止 

## 字典
1. 推导式： `{expr1: expr2 for item in iterable}` `{expr1: expr2 for (key, value) in iterable}` `{expr1: expr2  for (key, value) in iterable if condition}`
2. 创建： `{}` `dict(key=value)` `dict(zip(keys, values))` `dict.fromkeys(keys, value)` `dict.fromkeys(keys, value)` `dict.fromkeys(keys, value)`

