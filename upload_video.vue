<template>
  <a-layout class="layout">
    <a-layout-header>
      <div class="logo" />

      <video_header />


    </a-layout-header>
    <a-layout-content style="padding: 0 50px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>视频平台</a-breadcrumb-item>
        <a-breadcrumb-item>视频上传</a-breadcrumb-item>

      </a-breadcrumb>
      <div :style="{ background: '#fff', padding: '24px', minHeight: '280px' }">

      

      <a-upload :before-upload="beforeUpload"  @change="fileupload">



        <a-button>上传视频</a-button>


      </a-upload>


      <br />


      <video  v-if="src"  style="width:100%" height="300" :src="src"  controls="controls" >
        


      </video>


    

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


      // 视频地址变量
     src:"",

     // 分片个数
     shardCount:0,

     // 完成个数

     finished:0


    }
  },
   components:{

      "video_header":video_header

  },
  methods:{


    // 头像上传

    fileupload:function(file){


      console.log(file);


      // 获取文件的总大小

      var size = file.file.size;


      //console.log(size);

      // 定义一个切片大小

      var shardSize = 1024 * 1024;


      // 计算总片数

      var shardCount = Math.ceil(size / shardSize);

      console.log(shardCount)

      this.shardCount = shardCount;



      // 遍历切片

      for(var i=0;i<shardCount;++i){


          // 切片

          var start = i * shardSize;

          var end = Math.min(size,start + shardSize);


          // 开始切片

          var tinyfile = file.file.slice(start,end);




          // 请求后端接口

      let data = new FormData();

      data.append("file",tinyfile)

      data.append("count",i)

      const axios_upload = this.axios.create({withCredentials:false})


      axios_upload({

          method:"POST",
          url:"http://localhost:5000/upload/",
          data:data

      }).then(data => {


            console.log(data);

           // this.$message.info(data.data.msg);

            // 当上传成功，给图片地址赋值

            if(data.data.errcode == 0){

                  //this.src = "http://localhost:5000/static/"+  data.data.uid  + "/" + data.data.filename;

                  this.finished += 1;


                  if(this.finished == this.shardCount){



                        //this.$message.info(data.data.msg);

                        // 触发合并分片文件


                        this.myaxios("http://localhost:5000/upload/","put",{"filename":file.file.name}).then(data => {


                        // 判断当前用户是否具备无感知资格

                        if(data.errcode != 0){


                          this.$message.info(data.msg);


                          this.src = "http://localhost:5000/static/"+  data.data.uid  + "/" + data.data.filename;




                        }




                      })



                  }

         

            }

      })




      }



      



    },

    // 文件上传之前的校验

    beforeUpload:function(file){

        return false;

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