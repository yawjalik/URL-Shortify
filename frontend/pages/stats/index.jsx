import { useState, useEffect } from "react"
import { toast } from 'react-toastify'
import axios from 'axios'
import NavBar from "../../components/navbar"

const Stats = () => {
    const [text, setText] = useState("")
    const [stats, setStats] = useState([{url: "url", datetime_created: "date", shortened_url: "short"}])
    const [loading, setLoading] = useState(false)


    const getStats = async () => {
        const res = await axios.get('http://localhost:8000/stats')
                                .then(res => res.data)
                                .catch(() => toast.warning("No stats found"))
        console.log(res.data)
        setStats(res.data)
        console.log(stats)
    }

    useEffect(() => {
        // getStats()
        console.log(stats)
    }, [])
    

    const onClick = () => {
        if (text.length > 0) {
            setLoading(true)
            axios.get('http://localhost:8000/')
        } 
        else {
            getStats()
            console.log(stats)
        }
    }

    return <div className="text-center">
        <h1 className='text-4xl font-bold my-2'>Stats</h1>
        <NavBar/>
        

        <table className='table-auto divide-y divide-gray-200 w-full'>
            <thead className="bg-gray-50">
                <tr>
                    <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Date Created
                    </th>
                    <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Original URL
                    </th>
                    <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Shortened URL
                    </th>
                </tr>
            </thead>

            <tbody className="bg-white divide-y divide-gray-200">
                {stats.map((stat, index) => (
                    <tr key={index}>
                        <td className="px-6 py-4 whitespace-nowrap">
                            {stat.datetime_created}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                            {stat.url}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                            {stat.shortened_url}
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>

        <input className='bg-gray-200 rounded px-2 py-1 m-2' type="text" placeholder='Search URL stats by hash' value={text} onChange={e => setText(e.target.value)}/>
        <button disabled={loading} className="bg-blue-200 hover:bg-blue-300 rounded px-2 py-1 m-2" onClick={onClick}>
            {loading ? "Loading" : "Search"}
        </button>
    </div>
}

export default Stats