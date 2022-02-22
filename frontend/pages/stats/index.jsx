import { useState, useEffect } from "react"
import { toast } from 'react-toastify'
import NavBar from "../../components/navbar"
import apiService from "../../services/api"

const Stats = () => {
    const [urlInput, setUrlInput] = useState("")
    const [stats, setStats] = useState([])
    const [urlStat, setUrlStat] = useState({})
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        const getStats = async () => {
            const res = await apiService.getStats()
            setStats(res.data)
            // Handle network error
        }
        getStats()
    }, [])

    const onClick = () => {
        if (urlInput.length > 0) {
            setLoading(true)
            apiService.getStatByOriginalUrl(urlInput)
            .then(res => {
                setUrlStat(res.data)
            })
            .catch(() => toast.error("Invalid URL"))
            .finally(() => setLoading(false))
        }
    }

    return <div className="text-center">
        <h1 className='text-4xl font-bold my-2'>Statistics</h1>
        <NavBar/>
        <input className='bg-gray-200 rounded px-2 py-1 m-2' type="text" placeholder='Search URL stats by hash' value={urlInput} onChange={e => setUrlInput(e.target.value)}/>
        <button disabled={loading} className="bg-blue-200 hover:bg-blue-300 rounded px-2 py-1 m-2" onClick={onClick}>
            {loading ? "Loading" : "Search"}
        </button>

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

    </div>
}

export default Stats