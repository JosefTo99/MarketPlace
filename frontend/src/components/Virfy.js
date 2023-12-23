import { useState } from 'react'
import './vrify.css'

export default function Virfy() {

    const [code, setCode] = useState("")
    const sendCode = () => {
        fetch("http://127.0.0.1:8000/api/v1/auth/register/", {
            method: "POST",
            headers: {
                "content-Type": "Application/json",
            },
            body: JSON.stringify({
                code,
             
            })
        }).then((res) => res.json())
        .then((data) => {
            console.log(data)
            // navigate("/");
            // window.localStorage.setItem("email", email)
            window.location.pathname = "/virfy"
        })
    }

    return (
        <>
                <h1 className='title'>Firfyed your account</h1>
                <div className='perent-vrify'>
            <div className='container-vrify'>
                <input type="text" placeholder='Enter the code'
                onChange={(e) => {
                    setCode(e.target.value)
                }}
                />
                <button onClick={() => {
                    sendCode()
                }}>virfy</button>
            </div>
            </div>
        </>
    )
}