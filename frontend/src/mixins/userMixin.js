export default {
    data() {
      return {
        user: null,
        role: null,
        isLoggedin: false,
      };
    },
    async created() {
      // await this.checkAuth();
      await this.getUserDetails();
    },
    // watch: {
      // user(newVal) {
      //   if (!newVal) {
      //     // If user becomes null, meaning session expired or user is logged out
      //     alert('Session expired. Please log in again.');
      //     this.logout(); // Call the logout method to clear session
      //   }
      // },
    // },
    methods: {
      // async checkAuth(){
      //     const access_token = localStorage.getItem("access_token");
      //     if (!access_token) {
      //       this.isLoggedin = false;
      //       this.user = null;
      //       this.role = null;
      //       return;
      //     }
      //       try {
      //         this.user = await this.getUserDetails(); 
      //         this.isLoggedin = true;
      //         this.role = this.user.role;
      //         return this.user;
              
      //       } catch (error) {
      //         console.log(error);
      //       }       
      // },
      async getUserDetails() {
        if(!localStorage.getItem("access_token")) {
          // alert("Please log in to continue.");
          console.log("Please log in to continue.");
          // window.location.href = "/";
          
          return null;
        }
        try{
        const response = await fetch("http://127.0.0.1:5000/getuserdata", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
          },
        });   
          const data = await response.json();
          // console.log(data.message)
          if (!response.ok) {
            console.log(data.error);
            this.isLoggedin = false;
            this.user = null;
            this.role = null;
            return null;
          } else {
            console.log("In usermixin", data.user);
            this.isLoggedin = true;
            this.role = data.user.role;
            this.user = data.user;
            return data.user;
          }
      } catch (error) {
        console.log(error);
      }
      },
      async logout() {
        const response = await fetch("http://127.0.0.1:5000/logout", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json();
        if (!response.ok) {
          alert(data.error);
        }
        else{
          localStorage.removeItem("access_token");
          this.isLoggedin = false;
          this.user = null;
          this.role = null;
          // this.$router.push("/");
          window.location.href = "/";
        }
  
      },
       
    },
  };
  