<template>
  <a-layout class="layout">
    <a-layout-header>
      <div class="logo" />

      <video_header />


    </a-layout-header>
    <a-layout-content style="padding: 0 50px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>视频平台</a-breadcrumb-item>
        <a-breadcrumb-item>后台管理</a-breadcrumb-item>

      </a-breadcrumb>
      <div :style="{ background: '#fff', padding: '24px', minHeight: '280px' }">


        <a-form-item label="默认排序方式">


          <a-select  @change="get_userlist"  v-model:value="orderby" placeholder="请选择一个字段进行检索">
            

                <a-select-option value="a.id desc">倒序</a-select-option>

                <a-select-option value="a.id asc">正序</a-select-option>


          </a-select>
          


        </a-form-item>


        <a-form-item label="检索字段">


          <a-select  v-model:value="selected" placeholder="请选择一个字段进行检索">
            

                <a-select-option value="username">用户名</a-select-option>

                <a-select-option value="create_time">创建日期时间</a-select-option>

                <a-select-option value="rid">角色名称</a-select-option>


          </a-select>
          



        </a-form-item>


        <a-form-item label="查询关键字" >


              <a-input v-model:value="keyword"  @keyup.enter="get_userlist"  />

        </a-form-item>


        <a-button style="float:right;" @click="get_userlist"  >查 询</a-button>


        <br />


          <a-pagination v-model:current="current"  @change="get_userlist" :total="total" show-less-items  v-model:pageSize="pagesize" />



            <table style="width:100%" border="1">



              <tr>  <td>序号</td>  <td>用户名</td>  <td>创建时间</td>  <td>角色名称</td>  <td>操作</td>   </tr>



              <tr v-for="(item,index) in userlist">
                


                  <td> {{ index }}  </td>


                  <td> {{ item.username }}  </td>


                  <td> {{ item.create_time }}  </td>


                  <td> {{ item.rid }}  </td>


                  <td> <a-button>修 改</a-button> &nbsp;&nbsp; <a-button>删 除</a-button>  </td>



              </tr>
              






            </table>



            <a-pagination v-model:current="current"  @change="get_userlist"  :total="total" show-less-items  v-model:pageSize="pagesize" />

       


    

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


      // 用户列表
     userlist:"",

     // 关键字

     keyword:"",

     // 选中字段

     selected:"username",

     // 排序字段

     orderby:"a.id desc",


     // 总个数

     total:0,

     // 每页个数

     pagesize:0,

     // 当前页

     current:1


    }
  },
   components:{

      "video_header":video_header

  },
  methods:{


      // 获取用户列表页
      get_userlist:function(){


        this.myaxios("http://localhost:5000/admin_index/","get",{"keyword":this.keyword,"selected":this.selected,"orderby":this.orderby,"page":this.current}).then(data => {


                 

                          if(data.errcode == 0 ){



                                this.userlist = data.data;

                                // 赋值总个数

                                this.total = data.total;

                                // 赋值每页个数

                                this.pagesize = data.pagesize;



                          }
                  


            })



      },

      // 校验用户合法性
      check_token:function(){



          this.myaxios("http://localhost:5000/admin/","get").then(data => {


                 

                          if(data.errcode != 0 ){



                                this.$message.info(data.msg);


                                window.location.href = "/user_center";



                          }
                  


            })



      },
      

    

   


  },
  created(){  


    // 调用token检查

    this.check_token();


    // 调用获取用户列表


    this.get_userlist();


    this.$nextTick(() => {
    rabbit_init();
})




  }

}


</script>
<style>

td {

  padding:5px;

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