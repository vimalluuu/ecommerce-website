-- ============================================================
-- ARCFORM — Premium Streetwear E-Commerce Platform
-- Supabase / PostgreSQL Schema
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- USERS (extends Supabase auth.users)
-- ============================================================
CREATE TABLE IF NOT EXISTS public.users (
  id UUID PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  phone VARCHAR(20),
  avatar_url TEXT,
  is_admin BOOLEAN DEFAULT FALSE,
  is_email_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- ADDRESSES
-- ============================================================
CREATE TABLE IF NOT EXISTS public.addresses (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
  label VARCHAR(50) DEFAULT 'Home',
  street TEXT NOT NULL,
  city VARCHAR(100) NOT NULL,
  state VARCHAR(100) NOT NULL,
  postal_code VARCHAR(20) NOT NULL,
  country VARCHAR(100) DEFAULT 'India',
  is_default BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- CATEGORIES
-- ============================================================
CREATE TABLE IF NOT EXISTS public.categories (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(100) NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  image_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- PRODUCTS
-- ============================================================
CREATE TABLE IF NOT EXISTS public.products (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(200) NOT NULL,
  slug VARCHAR(200) UNIQUE NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  compare_price DECIMAL(10,2) CHECK (compare_price >= 0),
  stock INTEGER DEFAULT 0 CHECK (stock >= 0),
  category_id UUID REFERENCES public.categories(id) ON DELETE SET NULL,
  image_urls JSONB DEFAULT '[]',
  sizes JSONB DEFAULT '[]',
  colors JSONB DEFAULT '[]',
  tags JSONB DEFAULT '[]',
  is_featured BOOLEAN DEFAULT FALSE,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- COUPONS
-- ============================================================
CREATE TABLE IF NOT EXISTS public.coupons (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  code VARCHAR(50) UNIQUE NOT NULL,
  discount_type VARCHAR(20) DEFAULT 'percentage' CHECK (discount_type IN ('percentage', 'fixed')),
  discount_value DECIMAL(10,2) NOT NULL CHECK (discount_value > 0),
  min_order_amount DECIMAL(10,2) DEFAULT 0,
  max_uses INTEGER,
  uses_count INTEGER DEFAULT 0,
  expires_at TIMESTAMPTZ,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- ORDERS
-- ============================================================
CREATE TABLE IF NOT EXISTS public.orders (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_number VARCHAR(20) UNIQUE NOT NULL,
  user_id UUID REFERENCES public.users(id) ON DELETE SET NULL,
  total_amount DECIMAL(10,2) NOT NULL,
  discount_amount DECIMAL(10,2) DEFAULT 0,
  shipping_cost DECIMAL(10,2) DEFAULT 0,
  payment_status VARCHAR(50) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'failed', 'refunded')),
  order_status VARCHAR(50) DEFAULT 'processing' CHECK (order_status IN ('processing', 'confirmed', 'shipped', 'delivered', 'cancelled')),
  shipping_address JSONB NOT NULL,
  coupon_id UUID REFERENCES public.coupons(id) ON DELETE SET NULL,
  tracking_number VARCHAR(100),
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- ORDER ITEMS
-- ============================================================
CREATE TABLE IF NOT EXISTS public.order_items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id UUID REFERENCES public.orders(id) ON DELETE CASCADE,
  product_id UUID REFERENCES public.products(id) ON DELETE SET NULL,
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  size VARCHAR(20),
  color VARCHAR(50),
  price DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- WISHLIST
-- ============================================================
CREATE TABLE IF NOT EXISTS public.wishlist (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
  product_id UUID REFERENCES public.products(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, product_id)
);

-- ============================================================
-- REVIEWS
-- ============================================================
CREATE TABLE IF NOT EXISTS public.reviews (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
  product_id UUID REFERENCES public.products(id) ON DELETE CASCADE,
  rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
  review TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, product_id)
);

-- ============================================================
-- PERFORMANCE INDEXES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_products_category   ON public.products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_featured   ON public.products(is_featured) WHERE is_featured = TRUE;
CREATE INDEX IF NOT EXISTS idx_products_active     ON public.products(is_active)   WHERE is_active   = TRUE;
CREATE INDEX IF NOT EXISTS idx_products_slug       ON public.products(slug);
CREATE INDEX IF NOT EXISTS idx_orders_user         ON public.orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status       ON public.orders(order_status);
CREATE INDEX IF NOT EXISTS idx_orders_created_at   ON public.orders(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_order_items_order   ON public.order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_wishlist_user        ON public.wishlist(user_id);
CREATE INDEX IF NOT EXISTS idx_reviews_product     ON public.reviews(product_id);
CREATE INDEX IF NOT EXISTS idx_addresses_user      ON public.addresses(user_id);
CREATE INDEX IF NOT EXISTS idx_coupons_code        ON public.coupons(code);

-- ============================================================
-- AUTO UPDATED_AT TRIGGER
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON public.users
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_products_updated_at
  BEFORE UPDATE ON public.products
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_orders_updated_at
  BEFORE UPDATE ON public.orders
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================
ALTER TABLE public.users        ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.addresses    ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.wishlist     ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reviews      ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.orders       ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.order_items  ENABLE ROW LEVEL SECURITY;

-- Users: can only read/update their own row
CREATE POLICY "Users can view own profile"   ON public.users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.users FOR UPDATE USING (auth.uid() = id);

-- Addresses: users manage their own addresses
CREATE POLICY "Users manage own addresses" ON public.addresses
  USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

-- Wishlist: users manage their own wishlist
CREATE POLICY "Users manage own wishlist" ON public.wishlist
  USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

-- Reviews: users manage their own reviews
CREATE POLICY "Users manage own reviews" ON public.reviews
  USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

-- Reviews: anyone can read reviews
CREATE POLICY "Anyone can read reviews" ON public.reviews FOR SELECT USING (TRUE);

-- Orders: users see only their own orders
CREATE POLICY "Users view own orders" ON public.orders
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users create own orders" ON public.orders
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Order items: tied to order access
CREATE POLICY "Users view own order items" ON public.order_items
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM public.orders o
      WHERE o.id = order_id AND o.user_id = auth.uid()
    )
  );

-- Products & categories are publicly readable
CREATE POLICY "Anyone can read products"    ON public.products    FOR SELECT USING (TRUE);
CREATE POLICY "Anyone can read categories"  ON public.categories  FOR SELECT USING (TRUE);
ALTER TABLE public.products   ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.categories ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- SAMPLE SEED DATA
-- ============================================================
INSERT INTO public.categories (name, slug, description) VALUES
  ('Outerwear',    'outerwear',    'Premium jackets and coats'),
  ('Essentials',   'essentials',   'Core wardrobe staples'),
  ('Accessories',  'accessories',  'Bags, caps, and more')
ON CONFLICT (slug) DO NOTHING;
