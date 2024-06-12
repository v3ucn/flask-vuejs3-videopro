<template>
<div>


  

</div>
</template>


<script>
    

    export default {
 data() {
    return {


    }
  },
  methods:{


    

   


  },
  created(){  


        // 接收参数

        var username = this.$route.query.username;
        var token = this.$route.query.token;

        var refresh_token = this.$route.query.refresh_token;


        var avatar = this.$route.query.avatar;

        // 写入localstorage

        localStorage.setItem("username",username);

        localStorage.setItem("token",token);


        localStorage.setItem("refresh_token",refresh_token);


        if(typeof(avatar) != 'undefined'){

        localStorage.setItem("avatar",avatar);

        }

        // 跳转首页

        window.location.href = "/";



  }

}





</script>




<style>
    



</style>