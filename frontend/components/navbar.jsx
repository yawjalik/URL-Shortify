import Link from 'next/link'
import axios from 'axios'
import { toast } from 'react-toastify'

const NavBar = () => {

    const onClickHealth = () => {
        axios.get('http://localhost:8000/_healthcheck')
            .then(() => toast.success("API is alive"))
            .catch(() => toast.error("API is dead"))
    }

    return <nav className="flex justify-center flex-wrap my-8">
        <div>
            <Link href='/'>
                <a className='bg-blue-50 hover:bg-blue-100 rounded-md p-2 mx-2'>Home</a>
            </Link>
            <Link href='/stats'>
                <a className='bg-blue-50 hover:bg-blue-100 rounded-md p-2 mx-2'>URL Stats</a>
            </Link>
            <button className='bg-blue-50 hover:bg-blue-100 rounded-md p-2 mx-2' onClick={onClickHealth}>
                Health
            </button>
        </div>
    </nav>
}

export default NavBar