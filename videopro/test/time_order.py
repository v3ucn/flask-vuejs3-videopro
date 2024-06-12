# 时序算法的实现


# 时序的容器

s_dict = {0:[],1:[],2:[],3:[]}

# 时序key

s_key = 0


# 释放客服  客服uid

def release_user(uid):

    global s_key


    print(s_dict)


    for key in s_dict.keys():

        if uid in s_dict[key]:

            s_dict[key].remove(uid)

            s_dict[key-1].append(uid)

            if key == s_key:

                s_key -= 1






# 分配客服  客户uid

def send_user(uid):

    global s_key


    if s_key == 3:


        print("客服正忙，请稍后再试")

        return


    if len(s_dict[s_key]) == 1:


        s_dict[s_key+1].append(s_dict[s_key][0])

        cid = s_dict[s_key][0]

        s_dict[s_key].pop()

        s_key += 1



    else:

        # 还剩两个或者三个

        index = hash(uid) % len(s_dict[s_key])


        cid = s_dict[s_key][index]


        s_dict[s_key+1].append(s_dict[s_key][index])

        s_dict[s_key].pop(index)


    return cid


if __name__ == '__main__':
    
    print(send_user(10))

    print(s_dict)

    release_user(1)

    print(s_dict)

        










