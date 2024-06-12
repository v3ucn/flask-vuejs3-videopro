<template>
  <a-layout class="layout">
    <a-layout-header>
      <div class="logo" />

      <video_header />


    </a-layout-header>
    <a-layout-content style="padding: 0 50px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>视频平台</a-breadcrumb-item>
        <a-breadcrumb-item>登录</a-breadcrumb-item>

      </a-breadcrumb>
      <div :style="{ background: '#fff', padding: '24px', minHeight: '280px' }">




        <a-tabs v-model:activeKey="activeKey">
    

    <a-tab-pane key="1" tab="账密登录">


    <a-form-item  label="用户名" >


        <a-input  v-model:value="username"  placeholder="请输入用户名" />


      </a-form-item>


      <a-form-item  label="密 码" >


        <a-input  v-model:value="password"  placeholder="请输入密码" type="password" />


      </a-form-item>




  </a-tab-pane>




    <a-tab-pane key="2" tab="手机登录" force-render>
      

       <a-form-item  label="手机号" >


        <a-input  v-model:value="phone"  placeholder="请输入手机号"  />


      </a-form-item>


      <a-form-item  label="手机验证码" >


        <a-input  v-model:value="msg"  placeholder="请输入手机验证码" />

        

        <a-button  @click="send_code">发送短信</a-button>


      </a-form-item>



    </a-tab-pane>


  </a-tabs>



      <a-form-item  label="验证码" >


        <a-input  v-model:value="code"  placeholder="请输入验证码" />

        

        <a-button  @click="create_code">生成验证码</a-button>


        <img  v-if="src != ''" width="120" height="50"  :src="src" @click="refresh" />


      </a-form-item>



    

      <a-form-item   >


        <a-button @click="login">登 录</a-button>  &nbsp;&nbsp;


        <a-button @click="third_login('dingding')">钉钉登录</a-button>

        &nbsp;&nbsp;

        <a-button @click="third_login('gitee')">Gitee登录</a-button>


      </a-form-item>


    

    <div id="rabbit_box"></div>
    </div>
    </a-layout-content>
    <a-layout-footer style="text-align: center">
      视频社交平台
    </a-layout-footer>
  </a-layout>
</template>

<script>


import 'rabbit-widget/lib/rabbit.css';

var rabbit_init = require('rabbit-widget');

import video_header from './video_header.vue';


export default {
 data() {
    return {

     username:"",
     password:"",
     phone:"",

     // 输入的验证码
     code:"",
     // 图像文件流接口地址
     src:"",

     // 短信
     msg:"",

     activeKey:"1"


    }
  },
   components:{

      "video_header":video_header

  },
  methods:{


    // 三方登录按钮

    third_login:function(sitename){


        this.myaxios("http://localhost:5000/"+sitename+"_back/","post").then(data => {


                  console.log(data);

                  // 跳转

                  window.location.href = data.url;
                 


            })



    },
    // 发送短信
    send_code:function(){



      this.myaxios("http://localhost:5000/phone/","post",{"phone":this.phone}).then(data => {


                  console.log(data);


                  this.$message.info(data.msg);


            })





    },
    // 点击生成验证码

    create_code:function(){


        if(this.activeKey == "1" && this.username == ""){


            this.$message.info("用户名不能为空");

            return false;

            
        }


        if(this.activeKey == "2" && this.phone == ""){


            this.$message.info("手机号不能为空");

            return false;

            
        }


        if(this.activeKey == "1"){

            this.src = "http://localhost:5000/code/?username="+this.username

        }else{


          this.src = "http://localhost:5000/code/?username="+this.phone

        }





          


    },
      // 刷新方法

      refresh:function(){


         if(this.activeKey == "1"){

          this.src = "http://localhost:5000/code/" + "?username="+this.username+"&code=" + Math.ceil(Math.random()*100);

        }else{

this.src = "http://localhost:5000/code/" + "?username="+this.phone+"&code=" + Math.ceil(Math.random()*100);


        }

          console.log(this.src)



         

      },

      // 登录事件

      login:function(){


            console.log("开始登录");


            console.log(this.username);


            // 非空验证

            // if(this.username == ""){


            //   this.$message.info("您的用户名不能为空");

            //   return;


            // }


            // 调用请求

            this.myaxios("http://localhost:5000/user/","get",{"username":this.username,"password":this.password,"code":this.code,"phone":this.phone,"login_type":this.activeKey,"msg":this.msg}).then(data => {


                  console.log(data);


                  this.$message.info(data.msg);


                  if(data.errcode == 0){


                  // 存储用户名，用于展示

                  localStorage.setItem("username",data.username);

                  localStorage.setItem("token",data.token);

                  localStorage.setItem("refresh_token",data.refresh_token);



                  localStorage.setItem("avatar","http://localhost:5000/static/"+data.avatar);

                  // 跳转

                  window.location.href = "/";

                  }


            })


      }

    

   


  },
  created(){  


    this.$nextTick(() => {
    rabbit_init();
})




  }

}


</script>
<style>


img {


  cursor:pointer;

}


.site-layout-content {
  min-height: 280px;
  padding: 24px;
  background: #fff;
}
#components-layout-demo-top .logo {
  float: left;
  width: 120px;
  height: 31px;
  margin: 16px 24px 16px 0;
  background: rgba(255, 255, 255, 0.3);
}
.ant-row-rtl #components-layout-demo-top .logo {
  float: right;
  margin: 16px 0 16px 24px;
}

[data-theme='dark'] .site-layout-content {
  background: #141414;
}
</style>