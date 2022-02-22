import Link from 'next/link'
import { toast } from 'react-toastify'
import { useState } from 'react'
import apiService from '../services/api'

const NavBar = () => {
    const [loading, setLoading] = useState(false)

    const onClickHealth = () => {
        setLoading(true)
        apiService.getApiHealthCheck()
        .then(() => toast.success("API is alive"))
        .catch(() => toast.error("API is dead"))
        .finally(() => setLoading(false))
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
                {loading ? "Loading" : "Health"}
            </button>
        </div>
    </nav>
}

export default NavBar