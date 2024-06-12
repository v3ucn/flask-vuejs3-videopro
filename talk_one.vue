<template>
  <a-layout class="layout">
    <a-layout-header>
      <div class="logo" />

      <video_header />


    </a-layout-header>
    <a-layout-content style="padding: 0 50px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>视频平台</a-breadcrumb-item>
        <a-breadcrumb-item>私聊</a-breadcrumb-item>

      </a-breadcrumb>
      <div :style="{ background: '#fff', padding: '24px', minHeight: '280px' }">


    <h1>{{ username }}</h1>


    <br />


    <a-button @click="close_talk">关闭聊天</a-button>

    <br /><br />
      


      <span v-for="item,index in msglist">
        
        {{ item.username }} 说:

        
        <span v-if="item.msg_type == 1">
        {{ item.msg }}
        </span>  


        <span v-else-if="item.msg_type == 2">
          

          <video   style="width:100%" height="300" :src="'http://localhost:5000/static/'+item.msg"  controls="controls" >
        
          </video>

        </span>



        <span v-else-if="item.msg_type == 3">
          

          <img :src="'http://localhost:5000/static/'+item.msg"   />
        

        </span>


        <br /><br />

      </span>



      <br /><br />


      <a-textarea
      v-model:value="msg"
      placeholder="请输入您的聊天信息"
      :auto-size="{ minRows: 2, maxRows: 5 }"
    />


    <br /><br />


    <a-upload :before-upload="beforeUpload"  @change="fileupload">



        <a-button>发送文件</a-button>


      </a-upload>

      <br /><br />

    <a-button @click="send">发 送</a-button>


    

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

     // 重连标识
     lockReconnect:false,

     // 聊天内容

     msg:"",

     // 聊天记录

     msglist:[],

     // 聊天对象的uid

     uid:0,

     // 聊天对象名称

     username:"",

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

    // 释放聊天

    close_talk:function(){



      this.myaxios("http://localhost:5000/customer/","delete",{"uid":this.uid}).then(data => {


                  console.log(data);


                  window.opener = null;
                  window.open("about:blank", "_top").close();


            })




    },
    // 获取聊天记录

    get_msglist:function(){


        this.myaxios("http://localhost:5000/talk/","get",{"to_uid":this.uid}).then(data => {


                  console.log(data);

                  this.msglist = data.data;


              


            })


    },
    // 发送消息

    send:function(){



        this.myaxios("http://localhost:5000/talk/","post",{"msg":this.msg,"to_uid":this.uid}).then(data => {


                  console.log(data);


              


            })


    },
    // 重新链接websocket

    reconnect:function(){


        var that = this;

        if(that.lockReconnect){

            return;

        }

        that.lockReconnect = true;

        // 延时操作

        setTimeout(function(){

            that.init_websocket()

            that.lockReconnect = false;


        },5000)


    },
    // 链接websocket

    init_websocket:function(){


          var ws = new WebSocket("ws://localhost:5000/websocket/?token="+localStorage.getItem("token"));

          var that = this;

          // 链接建立
          ws.onopen = function(){

              console.log("websocket链接建立");

              ws.send("hello this is vue3");

          }

          // 接收消息

          ws.onmessage = function(evt){

                console.log(evt.data);

                // 数据类型转换

                try {


                  var msg = JSON.parse(evt.data);

                  console.log(msg["username"]);


                  that.msglist.push({"username":msg["username"],"msg":msg["msg"],"uid":msg["uid"],"msg_type":msg["msg_type"]});


                  console.log(that.msglist)





                 } catch {


                   that.$message.info(evt.data);

                 }
                

          }

          // 链接关闭

          ws.onclose = function(){


              console.log("websocket链接关闭");

              that.reconnect();

          }


    },
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

      //console.log(shardCount)

      this.shardCount = shardCount;


      var filename = file.file.name;

      console.log(filename);



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



                         // this.$message.info(data.msg);


                          //this.src = "http://localhost:5000/static/"+  data.data.uid  + "/" + data.data.filename;


                          console.log(data)


                          if( filename.match(/(.*)\.png/g)  == null){


                                  var msg_type = 2;

                          }else{



                                  var msg_type = 3;

                          }


                          // 发送消息

                          this.myaxios("http://localhost:5000/talk/","post",{"msg":data.uid+"/"+data.filename,"to_uid":this.uid,"msg_type":msg_type}).then(data => {


                  console.log(data);


              })


                        




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
      // 登录事件

      login:function(){


            console.log("开始登录");


            console.log(this.username);


            // 非空验证

            if(this.username == ""){


              this.$message.info("您的用户名不能为空");

              return;


            }


            // 调用请求

            this.myaxios("http://localhost:5000/user/","get",{"username":this.username,"password":this.password}).then(data => {


                  console.log(data);


                  this.$message.info(data.msg);


                  if(data.errcode == 0){


                  // 存储用户名，用于展示

                  localStorage.setItem("username",data.username);

                  localStorage.setItem("token",data.token);

                  // 跳转

                  window.location.href = "/";

                  }


            })


      }

    

   


  },
  created(){  


    // 调用token检查

    this.check_token();


    this.init_websocket();


    // 接收参数

    this.uid = this.$route.query.uid


    this.username = this.$route.query.username


    this.get_msglist();


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