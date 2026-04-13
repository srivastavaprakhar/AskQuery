"use client"

import React, { useEffect, useState } from "react"
import { supabase } from "../lib/supabase"

export default function SupabaseExamples() {
  const [posts, setPosts] = useState([])
  const [realtimeMsg, setRealtimeMsg] = useState(null)

  useEffect(() => {
    let mounted = true

    async function fetchPosts() {
      const { data, error } = await supabase.from("posts").select("*")
      if (!error && mounted) setPosts(data || [])
    }

    fetchPosts()

    const channel = supabase
      .channel("public:posts")
      .on("postgres_changes", { event: "INSERT", schema: "public", table: "posts" }, (payload) => {
        setRealtimeMsg(payload)
        setPosts((prev) => [payload.new, ...prev])
      })

    channel.subscribe()

    return () => {
      mounted = false
      channel.unsubscribe()
    }
  }, [])

  const uploadFile = async (file) => {
    if (!file) return
    const { data, error } = await supabase.storage.from("uploads").upload(file.name, file)
    if (error) throw error
    return data
  }

  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-lg font-semibold">Posts</h3>
        <ul className="list-disc pl-5">
          {posts.map((p) => (
            <li key={p.id}>{p.title ?? JSON.stringify(p)}</li>
          ))}
        </ul>
      </div>

      {realtimeMsg && (
        <div className="rounded-md bg-blue-50 p-2 text-sm">Realtime insert: {JSON.stringify(realtimeMsg)}</div>
      )}

      <div>
        <label className="block text-sm font-medium mb-1">Upload file to `uploads` bucket</label>
        <input
          type="file"
          onChange={(e) => uploadFile(e.target.files?.[0]).then(() => alert("Uploaded")).catch((err) => alert(err.message))}
        />
      </div>
    </div>
  )
}
