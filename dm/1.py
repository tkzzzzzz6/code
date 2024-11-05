import itertools


# 辅助函数:用于评估逻辑表达式
def eval_expr(expr, variables, values):
    # 用值替换变量
    for var, val in zip(variables, values):
        expr = expr.replace(var, str(val))
    # 将逻辑运算符替换为Python等效运算符
    expr = expr.replace('1', 'True').replace('0', 'False')
    expr = expr.replace('&', ' and ').replace('|', ' or ')
    expr = expr.replace('!', 'not ').replace('>', ' or not ')
    return eval(expr)


# 生成真值表并生成带索引项的详细DNF/CNF
def generate_truth_table(expr):
    # 提取唯一变量
    variables = sorted(set(filter(str.isalpha, expr)))
    num_vars = len(variables)

    # 生成所有可能的输入值组合
    combinations = list(itertools.product([1, 0], repeat=num_vars))
    results = []

    # 对每个组合评估表达式
    for values in combinations:
        result = eval_expr(expr, variables, values)
        results.append((values, result))

    # 推导DNF(最小项)和CNF(最大项)部分
    dnf_clauses = []
    cnf_clauses = []

    # 跟踪最小项和最大项索引
    minterm_idx = 0
    maxterm_idx = 0

    for values, result in results:
        # DNF: 仅包含结果为True的组合
        if result:
            minterm = []
            for var, val in zip(variables, values):
                minterm.append(f"{var}" if val == 1 else f"!{var}")
            dnf_clauses.append((f"m{minterm_idx}", " & ".join(minterm)))
            minterm_idx += 1

        # CNF: 仅包含结果为False的组合
        else:
            maxterm = []
            for var, val in zip(variables, values):
                maxterm.append(f"!{var}" if val == 1 else f"{var}")
            cnf_clauses.append((f"M{maxterm_idx}", " | ".join(maxterm)))
            maxterm_idx += 1

    # 组合DNF和CNF项以获得完整形式
    dnf_expr = " | ".join(f"({name}: {clause})" for name, clause in dnf_clauses) if dnf_clauses else "0"
    cnf_expr = " & ".join(f"({name}: {clause})" for name, clause in cnf_clauses) if cnf_clauses else "1"

    # 打印真值表
    print(f"表达式的真值表: {expr}")
    print(" | ".join(variables) + " | 结果")
    print("-" * (len(variables) * 4 + 10))

    for values, result in results:
        print(" | ".join(str(v) for v in values) + f" |   {int(result)}")

    # 打印每个DNF和CNF部分及其索引项
    print("\n主析取范式(DNF)各项(最小项):")
    for name, clause in dnf_clauses:
        print(f"{name}: ({clause})")

    print("\n主合取范式(CNF)各项(最大项):")
    for name, clause in cnf_clauses:
        print(f"{name}: ({clause})")

    # 打印完整的DNF和CNF表达式
    print("\n主析取范式(DNF):", dnf_expr)
    print("主合取范式(CNF):", cnf_expr)


# 主程序
if __name__ == "__main__":
    print("请输入逻辑表达式，使用以下符号:")
    print("& 表示与")
    print("| 表示或")
    print("! 表示非")
    print("> 表示蕴含")
    print("例如: (A & B) | (!A > C)")
    expression = input("请输入表达式: ")
    generate_truth_table(expression)