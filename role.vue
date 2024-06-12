<template>
  <a-layout class="layout">
    <a-layout-header>
      <div class="logo" />

      <video_header />


    </a-layout-header>
    <a-layout-content style="padding: 0 50px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>视频平台</a-breadcrumb-item>
        <a-breadcrumb-item>角色管理</a-breadcrumb-item>

      </a-breadcrumb>
      <div :style="{ background: '#fff', padding: '24px', minHeight: '280px' }">


          <a-form-item label="角色名称" >



            <a-input  v-model:value="name"  />


          </a-form-item>


          <a-button @click="add_role">添加新角色</a-button>




            <table style="width:100%" border="1">



              <tr>  <td>序号</td>  <td>角色名称</td>  <td>用户</td>  <td>操作</td>   </tr>



              <tr v-for="(item,index) in userlist">
                


                  <td> {{ index }}  </td>


                  <td> 


                
                <span v-if="editindex !==  index" >  {{ item.name }}  </span>


                <span  v-else >   <a-input :placeholder="item.name"   v-model:value="editname"   />     </span>  



                </td>

                  <td> {{ item.create_time }}  </td>


                  <td> 


                    <a-button  v-if="editindex !== index"  @click="edit_role(index)"  >修 改</a-button> 


                     <a-button v-else  @click="save_role(item.id)"  >保 存</a-button> 

                    &nbsp;&nbsp; 


                    <a-button @click="del(item.id)" >删 除</a-button>  </td>



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

     // 角色名称

     name:"",

     // 选中字段

     selected:"username",

     // 排序字段

     orderby:"a.id desc",


     // 总个数

     total:0,

     // 每页个数

     pagesize:0,

     // 当前页

     current:1,

     // 修改索引

     editindex:-1,

     // 修改角色名称

     editname:""


    }
  },
   components:{

      "video_header":video_header

  },
  methods:{

    // 保存角色
    save_role:function(id){



      this.myaxios("http://localhost:5000/admin_rolelist/","put",{"id":id,"name":this.editname}).then(data => {


                 

                          if(data.errcode == 0 ){



                                this.$message.info(data.msg);


                                this.userlist[this.editindex]["name"] = this.editname;


                                this.editindex = -1;



                          }
                  


            })




    },
    // 修改角色

    edit_role:function(index){



          this.editindex = index;



    },
    // 删除角色

    del:function(id) {
      
    
        console.log(id);


        this.myaxios("http://localhost:5000/admin_rolelist/","delete",{"id":id}).then(data => {


                 

                          if(data.errcode == 0 ){



                                this.$message.info(data.msg);



                                this.get_userlist()



                          }
                  


            })


    },

    // 添加新角色

    add_role:function(){



      this.myaxios("http://localhost:5000/admin_rolelist/","post",{"name":this.name}).then(data => {


                 

                          if(data.errcode == 0 ){



                                this.$message.info(data.msg);



                                this.get_userlist()



                          }
                  


            })




    },


      // 获取用户列表页
      get_userlist:function(){


        this.myaxios("http://localhost:5000/admin_rolelist/","get",{"keyword":this.keyword,"selected":this.selected,"orderby":this.orderby,"page":this.current}).then(data => {


                 

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