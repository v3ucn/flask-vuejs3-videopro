<template>
<div>

<span v-if="username != '' " style="color:white;">
  欢迎：{{ username }}  &nbsp;  


  <a-avatar size="large"  :src="src" >
    <template #icon>
        
    </template>
  </a-avatar>   

  &nbsp;&nbsp;&nbsp; 

  <span  v-for="item in menu">

  <a :href="item.url"  >{{ item.name }}</a>   &nbsp;&nbsp;&nbsp;  


  </span>



  <a href="#" @click="logout" >登 出</a>


</span>

<span  v-else >
<a href="/reg">注册</a> / <a href="/login">登录</a>
</span>

  

</div>
</template>



<script>
    



    export default {
 data() {
    return {

     username:"",
     src:localStorage.getItem("avatar"),
     menu:[]


    }
  },
  methods:{


    // 获取菜单

    get_menu:function(){


            this.myaxios("http://localhost:5000/admin/","post").then(data => {


                 

                          if(data.errcode == 0 ){



                                this.menu = data.menu;



                          }





                  


            })


    },

    // 登出
    logout:function(){

        
        localStorage.removeItem("username");
        localStorage.removeItem("token");

        window.location.href = "/login";



    },
    // 检测用户是否登录

    check_login:function(){


        var username = localStorage.getItem("username");

        if(username == null ){


                this.username = "";

        }else{


                this.username = username;

                this.get_menu()

        }


    }

   


  },
  created(){  


        // 调用是否登录方法

        this.check_login();

        console.log(this.username);



  }

}





</script>




<style>
    



</style>