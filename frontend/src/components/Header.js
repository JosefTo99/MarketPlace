import { Link } from "react-router-dom"

export default function Header() {
    const HendleLogOut = () => {
        window.localStorage.removeItem("email");
        window.location.pathname = "/"
    }

    return (
        <div className="container">
        <nav style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        }}>
            <div style={{display:"flex",}}>
           
            <Link to="/" style={{paddingRight:"10px"}}>Home</Link>
            <Link to="/about">About</Link>
            </div>
            <div style={{display:"flex",}}>
            {!window.localStorage.getItem("email") ? 
            <>
               <Link 
               to="/resgister" 
               style={{ textAlign: "center"}} 
               className="resgister-nav">
                     Register
                </Link>
                <Link to="/login" 
                style={{ textAlign: "center"}} 
                className="resgister-nav">
                     LogIn
                </Link> 
                </>
                : <div className="resgiater-nav" onClick={HendleLogOut}>Log Out</div>}
                </div>
        </nav>
        </div>
    )
}

