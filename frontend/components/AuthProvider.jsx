"use client"

import React, { createContext, useContext, useEffect, useState } from "react"
import { supabase, signOut } from "../lib/supabase"

const AuthContext = createContext({ user: null, signIn: async () => {}, signUp: async () => {}, signOut: async () => {} })

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)

  useEffect(() => {
    let mounted = true

    async function init() {
      const { data } = await supabase.auth.getUser()
      if (mounted) setUser(data?.user ?? null)
    }

    init()

    const { data: subscription } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    return () => {
      mounted = false
      subscription?.unsubscribe()
    }
  }, [])

  const signIn = (email, password) => supabase.auth.signInWithPassword({ email, password })
  const signUp = (email, password) => supabase.auth.signUp({ email, password })
  const signOutUser = async () => {
    await signOut()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, signIn, signUp, signOut: signOutUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
