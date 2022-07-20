def cleanLocalEnv(env, nodeArr) -> None:
    if len(nodeArr) == 0:
        return
    for _ in range(len(nodeArr)):
        if nodeArr[_] in env.keys():
            env.__delitem__(nodeArr[_])
    del nodeArr