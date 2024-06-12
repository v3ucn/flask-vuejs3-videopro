<template>
  <a-layout class="layout">
    <a-layout-header>
      <div class="logo" />

      


    </a-layout-header>
    <a-layout-content style="padding: 0 50px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>视频平台</a-breadcrumb-item>
        <a-breadcrumb-item>注册</a-breadcrumb-item>

      </a-breadcrumb>
      <div :style="{ background: '#fff', padding: '24px', minHeight: '280px' }">


      

      <a-form-item  label="用户名" >


        <a-input  v-model:value="username"  placeholder="请输入用户名" />


      </a-form-item>


      <a-form-item  label="密 码" >


        <a-input  v-model:value="password"  placeholder="请输入密码" type="password" />


      </a-form-item>


      <a-form-item  label="手机号" >


        <a-input  v-model:value="phone"  placeholder="请输入手机号"  />


      </a-form-item>


      <a-form-item   >


        <a-button @click="reg">提 交</a-button>


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


export default {
 data() {
    return {

     username:"",
     password:"",
     phone:""


    }
  },
  methods:{

      // 注册事件

      reg:function(){


            console.log("开始注册");


            console.log(this.username);


            // 非空验证

            if(this.username == ""){


              this.$message.info("您的用户名不能为空");

              return;


            }


            // 调用请求

            this.myaxios("http://localhost:5000/user/","post",{"username":this.username,"password":this.password,"phone":this.phone}).then(data => {


                  console.log(data);


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