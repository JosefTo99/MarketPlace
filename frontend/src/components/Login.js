import { useState } from "react";
// import axios from "axios";
export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setpassword] = useState("");
    const [accept, setAccept] = useState(false);
    // const [emailError, setEmailError] = useState("")

    const submit = async (e) => {
        let flag = true
        e.preventDefault();
        setAccept(true);
        if (password.length < 8)  {
           flag = false
        } else flag = true;
        // try {
        // if (flag) {
        //     // write the right one
        //    let res = await axios.post("http://127.0.0.1:8000/api/Login",{
        //         email: email,
        //         passwordword: password,
        //     })
        //     if (res.status === 200) {
        //         window.localStorage.setItem("email", email)
        //         window.location.pathname = "/"
        //     }
        // }
        // }catch(err) {
        //     setEmailError(err.response.status)
        // }
        if (flag) {
            fetch("http://127.0.0.1:8000/api/v1/auth/register/", {
                method: "POST",
                headers: {
                    "content-Type": "Application/json",
                },
                body: JSON.stringify({            
                    email,
                    password,
                })
            }).then((res) => res.json())
            .then((data) => {
                console.log(data)
                // navigate("/");
                window.localStorage.setItem("email", email)
                window.location.pathname = "/"
            })
        }
    }
    return (
        <div className="parent">
          <div className="resgister">
            <form onSubmit={submit}>
                <label htmlFor="email">E-mail</label>
                <input id="email" 
                type="email" 
                placeholder="Enter Your E-mail" 
                required
                value={email}
                onChange={(e) => {
                    setEmail(e.target.value)
                }}/>
                {/* {accept && emailError === 422 && <p className="error">This E-mail is not valed</p> } */}
                <label htmlFor="password">passwordword</label>
                <input id="password" 
                type="password" 
                placeholder="Enter Your passwordword" 
                value={password}
                onChange={(e) => {
                    setpassword(e.target.value)
                }}/>
                {password.length < 8 && accept && <p className="error">passwordword must be more than 8 Char</p>}
                <div style={{ textAlign: "center"}}>
                    <button type="submit">Log In</button>
                </div>
            </form>
          </div>
        </div>
    )
}