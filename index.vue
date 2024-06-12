<template>
  <a-layout class="layout">
    <a-layout-header>
      <div class="logo" />

      
      <video_header />


    </a-layout-header>
    <a-layout-content style="padding: 0 50px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>视频平台</a-breadcrumb-item>
        <a-breadcrumb-item>首页</a-breadcrumb-item>

      </a-breadcrumb>
      <div :style="{ background: '#fff', padding: '24px', minHeight: '280px' }">


        你好，这里时视频社交平台


    

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

     value:"",


    }
  },
  components:{

      "video_header":video_header

  },
  methods:{

  

    

   


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