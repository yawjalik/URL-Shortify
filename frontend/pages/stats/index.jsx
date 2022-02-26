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
            try {
                const res = await apiService.getStats()
                setStats(res.data)
            } catch (err) {
                toast.error("Network error")
            }
        }
        getStats()
    }, [])

    const onClick = () => {
        if (urlInput.length > 0) {
            setLoading(true)
            apiService.getStatByOriginalUrl(urlInput)
            .then(res => {
                setUrlStat(res.data.data)
            })
            .catch(() => toast.error("Invalid URL"))
            .finally(() => {
                setLoading(false)
                setUrlInput("")
            })
        }
    }

    return <div className="flex flex-col min-h-screen justify-around items-center text-center">
        <div>
            <h1 className='text-4xl font-bold my-2'>Statistics</h1>
            <NavBar/>
            <input className='bg-gray-200 rounded px-2 py-1' type="text" placeholder='Search URL stats by hash' value={urlInput} onChange={e => setUrlInput(e.target.value)}/>
            <button disabled={loading} className="bg-blue-200 hover:bg-blue-300 rounded px-2 py-1 m-2" onClick={onClick}>
                {loading ? "Loading" : "Search"}
            </button>
        </div>
        
        {Boolean(Object.keys(urlStat).length) && (
            <div className="bg-gray-100 rounded-lg px-10 py-5 flex flex-col items-center relative mt-5 mb-5">
                <div className="flex flex-col items-center">
                    <div className="flex space-x-5">
                        <div className="flex flex-col">
                            <div className="flex justify-between space-x-3">
                                <span>Original URL</span>
                                <span>:</span>
                            </div>
                            <div className="flex justify-between space-x-3">
                                <span>Shortened URL</span>
                                <span>:</span>
                            </div>
                            <div className="flex justify-between space-x-3">
                                <span>Times clicked</span>
                                <span>:</span>
                            </div>
                            <div className="flex justify-between space-x-3">
                                <span>Datetime created</span>
                                <span>:</span>
                            </div>
                        </div>
                        <div className="flex flex-col">
                            <span>{urlStat.url}</span>
                            <span><a className="text-blue-500" href={urlStat.shortened_url}>{urlStat.shortened_url}</a></span>
                            <span>{urlStat.number_of_clicks}</span>
                            <span>{urlStat.datetime_created}</span>
                        </div>
                    </div>
                </div>
            </div>
        )}

        <table className='table-auto divide-y divide-gray-200 w-full'>
            <thead className="bg-gray-50">
                <tr>
                    <th className="w-1/3 p-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Date Created
                    </th>
                    <th className="w-1/3 p-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Original URL
                    </th>
                    <th className="w-1/3 p-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Shortened URL
                    </th>
                </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
                {stats.map((stat, index) => (
                    <tr key={index}>
                        <td className="p-3 whitespace-nowrap">
                            {stat.datetime_created}
                        </td>
                        <td className="p-3 whitespace-nowrap">
                            {stat.url}
                        </td>
                        <td className="p-3 whitespace-nowrap">
                            <a className="text-blue-500" href={stat.shortened_url} target="_blank">{stat.shortened_url}</a>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
        
    </div>
}

export default Stats