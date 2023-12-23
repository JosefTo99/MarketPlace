import { useState } from "react"
// import axios from "axios";
// import { useNavigate } from "react-router-dom"

export default function SingUp() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setpassword] = useState("");
    const [repeat, setRepeat] = useState("");
    const [accept, setAccept] = useState(false);
    // const [emailError, setEmailError] = useState("")
    // let navigate = useNavigate()

    const submit =  (e) => {
        let flag = true
        e.preventDefault();
        setAccept(true);
        if (name === "" || password.length < 8 || repeat !== password)  {
           flag = false
        } else flag = true;
        
        if (flag) {
            // write the right one
            //  axios.post("http://http://localhost:9000/user",{
            //     name: name,
            //     email: email,
            //     passwordword: password,
            //     passwordword_confirmation: repeat,
            // })
            // .then((data)=> console.log(data))
            // if (res.status === 200) {
            //     window.localStorage.setItem("email", email)
            //     window.location.pathname = "/"
            // }
            fetch("http://127.0.0.1:8000/api/v1/auth/register/", {
                method: "POST",
                headers: {
                    "content-Type": "Application/json",
                },
                body: JSON.stringify({
                 
                    name,
                    email,
                    password,
                    repeat
                })
            }).then((res) => res.json())
            .then((data) => {
                console.log(data)
                // navigate("/");
                // window.localStorage.setItem("email", email)
                window.location.pathname = "/virfy"
            })
        }
    }
    return (
        <div className="parent">
          <div className="resgister">
            <form onSubmit={submit}>
                <label htmlFor="name">Name</label>
                <input id="name" 
                type="text" 
                placeholder="Enter Your Name" 
                value={name}
                onChange={(e) => {
                      setName(e.target.value)
                }}/>
                {name === "" && accept && <p className="error">UserName is Required</p>}
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
                placeholder="Enter Your password" 
                value={password}
                onChange={(e) => {
                    setpassword(e.target.value)
                }}/>
                {password.length < 8 && accept && <p className="error">passwordword must be more than 8 Char</p>}
                <label htmlFor="repeat">Repeat password</label>
                <input id="repeat" 
                type="password" 
                placeholder="Enter The Seem password" 
                value={repeat}
                onChange={(e) => {
                    setRepeat(e.target.value)
                }}/>
                {repeat !== password && accept &&  <p className="error">password does not match</p>}
                <div style={{ textAlign: "center"}}>
                    <button type="submit">Register</button>
                </div>
            </form>
          </div>
        </div>
    )
 }