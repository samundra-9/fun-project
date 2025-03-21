import React from 'react'
import { useState } from 'react'
import api from '../api'
import { useNavigate } from 'react-router-dom'
import { ACCESS_TOKEN,REFRESH_TOKEN } from '../constants'
import { formToJSON } from 'axios'
import LoadingIndicator from './LoadingIndicator'


export default function  ({route,method}) {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [loading,setLoading] = useState(false)
    const navigate = useNavigate()

    const name = method == 'login' ? 'login' : 'register'

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();
        try{
            const res = await api.post(route,{
                username,
                password
            })
            if(method === 'login'){
                localStorage.setItem(ACCESS_TOKEN,res.data.access)
                localStorage.setItem(REFRESH_TOKEN,res.data.refresh)
                navigate('/')
            } 
            else{
                navigate('/login')
            }
             

        }catch(error){
            console.log(error)
            alert('error: ' + error.message)
        }finally{
            setLoading(false)
        } 
       
    }
return ( 
<div className="flex items-center justify-center min-h-screen bg-gray-200">
    <form onSubmit={handleSubmit} className="flex flex-col items-center bg-white p-8 rounded shadow-lg w-96">
        <h1 className="text-3xl font-bold mb-6 capitalize text-gray-700">{name}</h1>
        <input 
            type="text" 
            value={username}  
            onChange={(e) => setUsername(e.target.value)} 
            placeholder="Username" 
            className="w-full p-3 mb-4 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input 
            type="password" 
            value={password}  
            onChange={(e) => setPassword(e.target.value)} 
            placeholder="Password" 
            className="w-full p-3 mb-4 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {
            loading && <LoadingIndicator/> 
        }
        <button 
            type="submit" 
            className={`w-full p-3 bg-blue-500 text-white rounded hover:bg-blue-600 transition ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
            disabled={loading}
        >
            {name}
        </button>
    </form>
</div>
)
}
