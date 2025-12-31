export interface User {
  id: number
  email: string
  full_name: string
  role: string
  bank_id?: number
  is_active: boolean
  is_verified: boolean
}

export interface Bank {
  id: number
  name: string
  license_number: string
  contact_email: string
  is_active: boolean
  is_approved: boolean
}

export interface Consumer {
  id: number
  first_name: string
  last_name: string
  date_of_birth: string
  email?: string
  is_frozen: boolean
}

export interface CreditReport {
  id: number
  consumer_id: number
  credit_score: number
  score_factors: Record<string, string>
  report_data: any
  generated_at: string
}

export interface CreditAccount {
  id: number
  consumer_id: number
  bank_id: number
  account_type: string
  account_status: string
  payment_status: string
  current_balance: number
  credit_limit?: number
}

