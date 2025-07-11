export async function getLoginDetails() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        return;
    }
    else{
    try {
        const response = await fetch("http://127.0.0.1:5000/getuserdata", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            },
        });
        const data = await response.json();
        if (!response.ok) {
            console.log(data.error);
            return;
        }
        return {'isLoggedin': true, 'role': data.user.role, 'user': data.user};
    } catch (error) {
        console.log(error);
    }
}
}