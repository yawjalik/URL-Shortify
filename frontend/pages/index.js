import { useState } from 'react'
import { toast } from 'react-toastify'
import NavBar from '../components/navbar'
import apiService from '../services/api'

export default function Home() {
  const [text, setText] = useState("")
  const [hash, setHash] = useState("")
  const [loading, setLoading] = useState(false)

  const onClick = () => {
    if (text.length > 0) {
      setLoading(true)
      apiService.shortenUrl(text)
      .then(res => {
        setHash(res.data.shortened_url)
        setLoading(false)
      })
      .catch(() => {
        setLoading(false)
          toast.error("Invalid URL or something else went wrong")
          setHash("")
      })
    }
  }

  return (
    <div className='flex flex-col min-h-screen justify-around items-center text-center'>
      <div>
        <h1 className='text-4xl font-bold'>URL Shortify</h1>
        <NavBar/>
      </div>

      <div>
        <input className='bg-gray-200 rounded px-2 py-1 m-2' type="text" placeholder='Enter URL to shorten' value={text} onChange={e => setText(e.target.value)}/>
        <button disabled={loading} className="bg-blue-200 hover:bg-blue-300 rounded px-2 py-1 m-2" onClick={onClick}>
          {loading ? "Loading" : "Shorten"}
        </button>
      </div>
      
      <div className={hash ? 'bg-slate-100 p-2 rounded' : ''}>
        <h2 className='text-2xl text-green-500 font-bold my-2'>{hash ? 'Success!': ''}</h2>
        <p className='text-xl my-2'>
          <a className='text-blue-500' href={hash} target='_blank'>{hash}</a>
        </p>
      </div>
    </div>
  )
}
