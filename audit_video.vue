<template>
  <a-layout class="layout">
    <a-layout-header>
      <div class="logo" />

      <video_header />


    </a-layout-header>
    <a-layout-content style="padding: 0 50px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>视频平台</a-breadcrumb-item>
        <a-breadcrumb-item>视频审核</a-breadcrumb-item>

      </a-breadcrumb>
      <div :style="{ background: '#fff', padding: '24px', minHeight: '280px' }">


        <table>
          

            <tr>

              <td> 视频信息 </td>  <td> 发布者 </td>  <td> 操作 </td>
              
            </tr>


            <tr v-for="(item,index) in videolist">


              <td> 

                <video :src="'http://localhost:5000/static/'+item.id+'/'+item.src" > </video>


              </td>


              <td>
                

                {{ item.uid }}


              </td>


              <td>
                

                <a-button>审核通过</a-button>  / <a-button>审核拒绝</a-button>


              </td>
              


            </tr>



        </table>





    

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


      // 图片地址变量
     src:"",
     videolist:[]


    }
  },
   components:{

      "video_header":video_header

  },
  methods:{

    // 获取视频
    get_data:function(){



      this.myaxios("http://localhost:5000/audit/","get").then(data => {


                  console.log(data);


                  this.videolist = data.data;



            })





    },
      // 校验用户合法性
      check_token:function(){



          this.myaxios("http://localhost:5000/userinfo/","get").then(data => {


                  console.log(data);


                  // 赋值头像

                  this.src = "http://localhost:5000/static/" + data.filename;


                  // 判断

                  if(data.errcode != 0 ){


                      // this.$message.info(data.msg);

                      // localStorage.removeItem("token");
                      // localStorage.removeItem("username");

                      // window.location.href = "/login";



                      // 请求后端接口检查当前用户的refresh_token

                      this.myaxios("http://localhost:5000/userinfo/","put",{"refresh_token":localStorage.getItem("refresh_token")}).then(data => {


                        // 判断当前用户是否具备无感知资格

                        if(data.errcode != 0){


                          this.$message.info(data.msg);

                      localStorage.removeItem("token");
                      localStorage.removeItem("username");
                      localStorage.removeItem("refresh_token");

                      window.location.href = "/login";




                        }




                      })







                  }


            })



      },
     

    

   


  },
  created(){  


    // 调用token检查

    this.check_token();


    this.get_data();


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