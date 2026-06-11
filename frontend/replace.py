import os, glob, re

base_dir = 'f:/ecommerce-website/frontend/pages'

replacements = {
    'admin/dashboard.html': '''
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="bg-gray-900 p-6 rounded-sm border border-gray-800">
                <h3 class="text-gray-500 font-mono text-xs uppercase tracking-widest mb-2">Total Revenue</h3>
                <p class="text-3xl font-display text-white">$124,500</p>
            </div>
            <div class="bg-gray-900 p-6 rounded-sm border border-gray-800">
                <h3 class="text-gray-500 font-mono text-xs uppercase tracking-widest mb-2">Orders</h3>
                <p class="text-3xl font-display text-white">842</p>
            </div>
            <div class="bg-gray-900 p-6 rounded-sm border border-gray-800">
                <h3 class="text-gray-500 font-mono text-xs uppercase tracking-widest mb-2">Customers</h3>
                <p class="text-3xl font-display text-white">1,204</p>
            </div>
            <div class="bg-gray-900 p-6 rounded-sm border border-gray-800">
                <h3 class="text-gray-500 font-mono text-xs uppercase tracking-widest mb-2">Conversion</h3>
                <p class="text-3xl font-display text-white">3.2%</p>
            </div>
        </div>
        <div class="bg-gray-900 p-8 rounded-sm border border-gray-800">
            <h2 class="font-display text-xl mb-6 uppercase tracking-wider">Recent Orders</h2>
            <table class="w-full text-left text-sm">
                <thead class="text-gray-500 font-mono text-xs uppercase tracking-widest border-b border-gray-800">
                    <tr>
                        <th class="pb-4">Order ID</th>
                        <th class="pb-4">Customer</th>
                        <th class="pb-4">Date</th>
                        <th class="pb-4">Total</th>
                        <th class="pb-4">Status</th>
                    </tr>
                </thead>
                <tbody class="text-gray-300">
                    <tr class="border-b border-gray-800">
                        <td class="py-4">#ORD-092</td>
                        <td class="py-4">Sarah Jenkins</td>
                        <td class="py-4">Today, 10:42 AM</td>
                        <td class="py-4">$340.00</td>
                        <td class="py-4 text-accent">Processing</td>
                    </tr>
                    <tr class="border-b border-gray-800">
                        <td class="py-4">#ORD-091</td>
                        <td class="py-4">Michael Chen</td>
                        <td class="py-4">Yesterday</td>
                        <td class="py-4">$1,250.00</td>
                        <td class="py-4 text-success">Shipped</td>
                    </tr>
                    <tr>
                        <td class="py-4">#ORD-090</td>
                        <td class="py-4">Elena Rostova</td>
                        <td class="py-4">Oct 24, 2025</td>
                        <td class="py-4">$890.00</td>
                        <td class="py-4 text-success">Delivered</td>
                    </tr>
                </tbody>
            </table>
        </div>
''',
    'admin/analytics.html': '''
        <div class="bg-gray-900 p-8 rounded-sm border border-gray-800 mb-8 h-64 flex items-center justify-center">
            <p class="text-gray-500 font-mono uppercase tracking-widest">[ Sales Chart Placeholder ]</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="bg-gray-900 p-8 rounded-sm border border-gray-800 h-64 flex items-center justify-center">
                <p class="text-gray-500 font-mono uppercase tracking-widest">[ Traffic Sources Placeholder ]</p>
            </div>
            <div class="bg-gray-900 p-8 rounded-sm border border-gray-800 h-64 flex items-center justify-center">
                <p class="text-gray-500 font-mono uppercase tracking-widest">[ Top Products Placeholder ]</p>
            </div>
        </div>
''',
    'admin/categories.html': '''
        <div class="flex justify-end mb-6">
            <button class="bg-white text-black px-6 py-2 font-mono text-xs uppercase tracking-widest hover:bg-accent transition-colors">+ New Category</button>
        </div>
        <div class="bg-gray-900 p-8 rounded-sm border border-gray-800">
            <table class="w-full text-left text-sm">
                <thead class="text-gray-500 font-mono text-xs uppercase tracking-widest border-b border-gray-800">
                    <tr>
                        <th class="pb-4">Name</th>
                        <th class="pb-4">Products Count</th>
                        <th class="pb-4">Status</th>
                        <th class="pb-4">Actions</th>
                    </tr>
                </thead>
                <tbody class="text-gray-300">
                    <tr class="border-b border-gray-800">
                        <td class="py-4 font-display text-lg text-white">Outerwear</td>
                        <td class="py-4">24</td>
                        <td class="py-4 text-success">Active</td>
                        <td class="py-4"><a href="#" class="text-accent hover:text-white">Edit</a></td>
                    </tr>
                    <tr class="border-b border-gray-800">
                        <td class="py-4 font-display text-lg text-white">Essentials</td>
                        <td class="py-4">42</td>
                        <td class="py-4 text-success">Active</td>
                        <td class="py-4"><a href="#" class="text-accent hover:text-white">Edit</a></td>
                    </tr>
                    <tr>
                        <td class="py-4 font-display text-lg text-white">Accessories</td>
                        <td class="py-4">15</td>
                        <td class="py-4 text-success">Active</td>
                        <td class="py-4"><a href="#" class="text-accent hover:text-white">Edit</a></td>
                    </tr>
                </tbody>
            </table>
        </div>
''',
    'admin/customers.html': '''
        <div class="bg-gray-900 p-8 rounded-sm border border-gray-800">
            <table class="w-full text-left text-sm">
                <thead class="text-gray-500 font-mono text-xs uppercase tracking-widest border-b border-gray-800">
                    <tr>
                        <th class="pb-4">Name</th>
                        <th class="pb-4">Email</th>
                        <th class="pb-4">Orders</th>
                        <th class="pb-4">Total Spent</th>
                    </tr>
                </thead>
                <tbody class="text-gray-300">
                    <tr class="border-b border-gray-800">
                        <td class="py-4 text-white">Sarah Jenkins</td>
                        <td class="py-4 text-gray-500">sarah.j@example.com</td>
                        <td class="py-4">4</td>
                        <td class="py-4">$1,240.00</td>
                    </tr>
                    <tr class="border-b border-gray-800">
                        <td class="py-4 text-white">Michael Chen</td>
                        <td class="py-4 text-gray-500">m.chen@example.com</td>
                        <td class="py-4">1</td>
                        <td class="py-4">$1,250.00</td>
                    </tr>
                </tbody>
            </table>
        </div>
''',
    'admin/orders.html': '''
        <div class="bg-gray-900 p-8 rounded-sm border border-gray-800">
            <table class="w-full text-left text-sm">
                <thead class="text-gray-500 font-mono text-xs uppercase tracking-widest border-b border-gray-800">
                    <tr>
                        <th class="pb-4">Order ID</th>
                        <th class="pb-4">Date</th>
                        <th class="pb-4">Customer</th>
                        <th class="pb-4">Total</th>
                        <th class="pb-4">Payment</th>
                        <th class="pb-4">Status</th>
                    </tr>
                </thead>
                <tbody class="text-gray-300">
                    <tr class="border-b border-gray-800">
                        <td class="py-4">#ORD-092</td>
                        <td class="py-4">Today</td>
                        <td class="py-4">Sarah Jenkins</td>
                        <td class="py-4">$340.00</td>
                        <td class="py-4 text-success">Paid</td>
                        <td class="py-4 text-accent">Processing</td>
                    </tr>
                    <tr class="border-b border-gray-800">
                        <td class="py-4">#ORD-091</td>
                        <td class="py-4">Yesterday</td>
                        <td class="py-4">Michael Chen</td>
                        <td class="py-4">$1,250.00</td>
                        <td class="py-4 text-success">Paid</td>
                        <td class="py-4 text-success">Shipped</td>
                    </tr>
                </tbody>
            </table>
        </div>
''',
    'admin/products.html': '''
        <div class="flex justify-end mb-6">
            <button class="bg-white text-black px-6 py-2 font-mono text-xs uppercase tracking-widest hover:bg-accent transition-colors">+ New Product</button>
        </div>
        <div class="bg-gray-900 p-8 rounded-sm border border-gray-800">
            <table class="w-full text-left text-sm">
                <thead class="text-gray-500 font-mono text-xs uppercase tracking-widest border-b border-gray-800">
                    <tr>
                        <th class="pb-4">Product</th>
                        <th class="pb-4">Category</th>
                        <th class="pb-4">Price</th>
                        <th class="pb-4">Inventory</th>
                        <th class="pb-4">Status</th>
                    </tr>
                </thead>
                <tbody class="text-gray-300">
                    <tr class="border-b border-gray-800">
                        <td class="py-4 flex items-center gap-4">
                            <div class="w-12 h-16 bg-gray-800"></div>
                            <span class="font-display text-white">Void Nylon Bomber</span>
                        </td>
                        <td class="py-4">Outerwear</td>
                        <td class="py-4">$340.00</td>
                        <td class="py-4">42 in stock</td>
                        <td class="py-4 text-success">Active</td>
                    </tr>
                    <tr class="border-b border-gray-800">
                        <td class="py-4 flex items-center gap-4">
                            <div class="w-12 h-16 bg-gray-800"></div>
                            <span class="font-display text-white">Heavyweight Hoodie</span>
                        </td>
                        <td class="py-4">Essentials</td>
                        <td class="py-4">$180.00</td>
                        <td class="py-4 text-error">2 in stock</td>
                        <td class="py-4 text-success">Active</td>
                    </tr>
                </tbody>
            </table>
        </div>
''',
    'auth/forgot-password.html': '''
        <div class="max-w-md mx-auto bg-gray-900 p-8 rounded-sm border border-gray-800 mt-12">
            <p class="text-gray-400 mb-6">Enter your email address and we will send you a link to reset your password.</p>
            <form class="flex flex-col gap-6">
                <div class="flex flex-col gap-2">
                    <label class="font-mono text-xs uppercase tracking-widest text-gray-500">Email Address</label>
                    <input type="email" class="bg-transparent border-b border-gray-700 py-2 text-white focus:outline-none focus:border-accent transition-colors" required>
                </div>
                <button type="submit" class="bg-white text-black py-4 font-mono text-sm uppercase tracking-widest hover:bg-accent transition-colors mt-4">Send Reset Link</button>
            </form>
            <div class="mt-8 text-center">
                <a href="login.html" class="text-gray-500 text-sm hover:text-accent transition-colors">Return to Login</a>
            </div>
        </div>
''',
    'auth/verify-email.html': '''
        <div class="max-w-md mx-auto bg-gray-900 p-12 rounded-sm border border-gray-800 mt-12 text-center">
            <div class="w-16 h-16 rounded-full border-2 border-accent text-accent flex items-center justify-center mx-auto mb-6 text-2xl">✓</div>
            <h2 class="font-display text-2xl mb-4 text-white">Check your email</h2>
            <p class="text-gray-400 mb-8">We've sent a verification link to your email address. Please click the link to activate your account.</p>
            <button class="bg-transparent border border-gray-700 text-white py-3 px-8 font-mono text-xs uppercase tracking-widest hover:border-accent hover:text-accent transition-colors">Resend Email</button>
        </div>
''',
    'public/privacy.html': '''
        <div class="max-w-3xl mx-auto prose prose-invert prose-p:text-gray-400 prose-headings:font-display prose-headings:font-normal prose-a:text-accent">
            <p>Last updated: June 2025</p>
            <h2 class="text-2xl mt-8 mb-4 text-white">1. Information We Collect</h2>
            <p>We collect information you provide directly to us, such as when you create or modify your account, request on-demand services, contact customer support, or otherwise communicate with us. This information may include: name, email, phone number, postal address, profile picture, payment method, items requested, delivery notes, and other information you choose to provide.</p>
            <h2 class="text-2xl mt-8 mb-4 text-white">2. How We Use Your Information</h2>
            <p>We may use the information we collect about you to provide, maintain, and improve our Services, including, for example, to facilitate payments, send receipts, provide products and services you request, develop new features, provide customer support, and send updates and administrative messages.</p>
            <h2 class="text-2xl mt-8 mb-4 text-white">3. Information Sharing</h2>
            <p>We do not share your personal information with third parties except as described in this privacy policy. We may share your information with our vendors, consultants, marketing partners, and other service providers who need access to such information to carry out work on our behalf.</p>
        </div>
''',
    'public/terms.html': '''
        <div class="max-w-3xl mx-auto prose prose-invert prose-p:text-gray-400 prose-headings:font-display prose-headings:font-normal prose-a:text-accent">
            <p>Last updated: June 2025</p>
            <h2 class="text-2xl mt-8 mb-4 text-white">1. Agreement to Terms</h2>
            <p>By accessing our website and purchasing our products, you agree to be bound by these Terms of Service and all applicable laws and regulations. If you do not agree with any of these terms, you are prohibited from using or accessing this site.</p>
            <h2 class="text-2xl mt-8 mb-4 text-white">2. Use License</h2>
            <p>Permission is granted to temporarily download one copy of the materials (information or software) on ARCFORM's website for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title.</p>
            <h2 class="text-2xl mt-8 mb-4 text-white">3. Disclaimer</h2>
            <p>The materials on ARCFORM's website are provided on an 'as is' basis. ARCFORM makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.</p>
        </div>
''',
    'user/checkout.html': '''
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <div>
                <h2 class="font-mono text-sm uppercase tracking-widest text-gray-500 mb-6">1. Shipping Address</h2>
                <form class="flex flex-col gap-6 mb-12">
                    <div class="grid grid-cols-2 gap-6">
                        <div class="flex flex-col gap-2">
                            <label class="font-mono text-xs uppercase tracking-widest text-gray-500">First Name</label>
                            <input type="text" class="bg-transparent border-b border-gray-700 py-2 text-white focus:outline-none focus:border-accent">
                        </div>
                        <div class="flex flex-col gap-2">
                            <label class="font-mono text-xs uppercase tracking-widest text-gray-500">Last Name</label>
                            <input type="text" class="bg-transparent border-b border-gray-700 py-2 text-white focus:outline-none focus:border-accent">
                        </div>
                    </div>
                    <div class="flex flex-col gap-2">
                        <label class="font-mono text-xs uppercase tracking-widest text-gray-500">Address</label>
                        <input type="text" class="bg-transparent border-b border-gray-700 py-2 text-white focus:outline-none focus:border-accent">
                    </div>
                    <div class="grid grid-cols-2 gap-6">
                        <div class="flex flex-col gap-2">
                            <label class="font-mono text-xs uppercase tracking-widest text-gray-500">City</label>
                            <input type="text" class="bg-transparent border-b border-gray-700 py-2 text-white focus:outline-none focus:border-accent">
                        </div>
                        <div class="flex flex-col gap-2">
                            <label class="font-mono text-xs uppercase tracking-widest text-gray-500">Postal Code</label>
                            <input type="text" class="bg-transparent border-b border-gray-700 py-2 text-white focus:outline-none focus:border-accent">
                        </div>
                    </div>
                </form>

                <h2 class="font-mono text-sm uppercase tracking-widest text-gray-500 mb-6">2. Payment Method</h2>
                <div class="bg-gray-900 border border-gray-800 p-6 rounded-sm flex flex-col gap-4">
                    <div class="flex items-center gap-4">
                        <input type="radio" name="payment" id="cc" checked class="accent-accent">
                        <label for="cc" class="text-white">Credit Card</label>
                    </div>
                    <div class="flex flex-col gap-2 mt-2">
                        <input type="text" placeholder="Card Number" class="bg-transparent border border-gray-700 p-3 text-white focus:outline-none focus:border-accent w-full">
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <input type="text" placeholder="MM/YY" class="bg-transparent border border-gray-700 p-3 text-white focus:outline-none focus:border-accent">
                        <input type="text" placeholder="CVC" class="bg-transparent border border-gray-700 p-3 text-white focus:outline-none focus:border-accent">
                    </div>
                </div>
            </div>
            
            <div class="bg-gray-900 p-8 border border-gray-800 h-fit">
                <h2 class="font-display text-xl mb-6 text-white">Order Summary</h2>
                <div class="flex flex-col gap-4 mb-6 pb-6 border-b border-gray-800">
                    <div class="flex justify-between">
                        <div class="text-gray-400">Void Nylon Bomber (M)</div>
                        <div class="text-white font-mono">$340.00</div>
                    </div>
                    <div class="flex justify-between">
                        <div class="text-gray-400">Heavyweight Hoodie (L)</div>
                        <div class="text-white font-mono">$180.00</div>
                    </div>
                </div>
                <div class="flex justify-between mb-2 text-sm">
                    <div class="text-gray-500">Subtotal</div>
                    <div class="text-white font-mono">$520.00</div>
                </div>
                <div class="flex justify-between mb-6 text-sm">
                    <div class="text-gray-500">Shipping</div>
                    <div class="text-white font-mono">$15.00</div>
                </div>
                <div class="flex justify-between items-center pt-6 border-t border-gray-800">
                    <div class="text-white font-display text-xl">Total</div>
                    <div class="text-accent font-mono text-xl">$535.00</div>
                </div>
                <button class="w-full bg-white text-black py-4 mt-8 font-mono text-sm uppercase tracking-widest hover:bg-accent transition-colors">Place Order</button>
            </div>
        </div>
''',
    'user/dashboard.html': '''
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="md:col-span-1">
                <div class="bg-gray-900 border border-gray-800 p-8 rounded-sm">
                    <div class="w-20 h-20 bg-gray-800 rounded-full mx-auto mb-4"></div>
                    <h3 class="text-center font-display text-xl text-white mb-1">Michael Chen</h3>
                    <p class="text-center text-gray-500 text-sm mb-8">m.chen@example.com</p>
                    
                    <nav class="flex flex-col gap-2">
                        <a href="dashboard.html" class="py-3 px-4 bg-gray-800 text-accent font-mono text-xs uppercase tracking-widest">Dashboard</a>
                        <a href="orders.html" class="py-3 px-4 text-gray-400 hover:text-white font-mono text-xs uppercase tracking-widest transition-colors">Orders</a>
                        <a href="wishlist.html" class="py-3 px-4 text-gray-400 hover:text-white font-mono text-xs uppercase tracking-widest transition-colors">Wishlist</a>
                        <a href="profile.html" class="py-3 px-4 text-gray-400 hover:text-white font-mono text-xs uppercase tracking-widest transition-colors">Profile</a>
                    </nav>
                </div>
            </div>
            <div class="md:col-span-2 flex flex-col gap-8">
                <div class="grid grid-cols-2 gap-6">
                    <div class="bg-gray-900 border border-gray-800 p-6 rounded-sm">
                        <h4 class="text-gray-500 font-mono text-xs uppercase tracking-widest mb-2">Total Orders</h4>
                        <p class="font-display text-3xl text-white">12</p>
                    </div>
                    <div class="bg-gray-900 border border-gray-800 p-6 rounded-sm">
                        <h4 class="text-gray-500 font-mono text-xs uppercase tracking-widest mb-2">Wishlist Items</h4>
                        <p class="font-display text-3xl text-white">4</p>
                    </div>
                </div>
                <div class="bg-gray-900 border border-gray-800 p-8 rounded-sm">
                    <h3 class="font-display text-xl text-white mb-6">Recent Activity</h3>
                    <div class="flex flex-col gap-4 text-sm">
                        <div class="flex justify-between border-b border-gray-800 pb-4">
                            <div class="text-gray-300">Order <span class="text-accent">#ORD-091</span> shipped</div>
                            <div class="text-gray-500 font-mono text-xs">Yesterday</div>
                        </div>
                        <div class="flex justify-between border-b border-gray-800 pb-4">
                            <div class="text-gray-300">Added Void Bomber to Wishlist</div>
                            <div class="text-gray-500 font-mono text-xs">Oct 24</div>
                        </div>
                        <div class="flex justify-between">
                            <div class="text-gray-300">Order <span class="text-white">#ORD-085</span> delivered</div>
                            <div class="text-gray-500 font-mono text-xs">Sep 12</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
''',
    'user/order-detail.html': '''
        <a href="orders.html" class="text-gray-500 font-mono text-xs uppercase tracking-widest hover:text-accent transition-colors mb-8 inline-block">← Back to Orders</a>
        <div class="bg-gray-900 border border-gray-800 p-8 rounded-sm mb-8">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8 pb-8 border-b border-gray-800">
                <div>
                    <h2 class="font-display text-2xl text-white mb-1">Order #ORD-091</h2>
                    <p class="text-gray-500 font-mono text-xs uppercase tracking-widest">Placed on Yesterday, 10:42 AM</p>
                </div>
                <div class="bg-success text-black px-4 py-1 font-mono text-xs uppercase tracking-widest">Shipped</div>
            </div>
            
            <h3 class="font-mono text-sm uppercase tracking-widest text-gray-500 mb-6">Items</h3>
            <div class="flex flex-col gap-6 mb-8 pb-8 border-b border-gray-800">
                <div class="flex gap-6 items-center">
                    <div class="w-16 h-20 bg-gray-800"></div>
                    <div class="flex-1">
                        <h4 class="font-display text-lg text-white">Void Nylon Bomber</h4>
                        <p class="text-gray-500 text-sm">Size: M | Color: Black</p>
                    </div>
                    <div class="font-mono text-accent">$340.00</div>
                </div>
            </div>
            
            <div class="flex flex-col gap-2 max-w-xs ml-auto">
                <div class="flex justify-between text-sm">
                    <span class="text-gray-500">Subtotal</span>
                    <span class="text-white font-mono">$340.00</span>
                </div>
                <div class="flex justify-between text-sm">
                    <span class="text-gray-500">Shipping</span>
                    <span class="text-white font-mono">$15.00</span>
                </div>
                <div class="flex justify-between pt-4 mt-2 border-t border-gray-800">
                    <span class="text-white font-display text-lg">Total</span>
                    <span class="text-accent font-mono text-lg">$355.00</span>
                </div>
            </div>
        </div>
''',
    'user/orders.html': '''
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="md:col-span-1">
                <nav class="flex flex-col gap-2 bg-gray-900 border border-gray-800 p-4 rounded-sm">
                    <a href="dashboard.html" class="py-3 px-4 text-gray-400 hover:text-white font-mono text-xs uppercase tracking-widest transition-colors">Dashboard</a>
                    <a href="orders.html" class="py-3 px-4 bg-gray-800 text-accent font-mono text-xs uppercase tracking-widest">Orders</a>
                    <a href="wishlist.html" class="py-3 px-4 text-gray-400 hover:text-white font-mono text-xs uppercase tracking-widest transition-colors">Wishlist</a>
                    <a href="profile.html" class="py-3 px-4 text-gray-400 hover:text-white font-mono text-xs uppercase tracking-widest transition-colors">Profile</a>
                </nav>
            </div>
            <div class="md:col-span-3">
                <div class="bg-gray-900 border border-gray-800 p-8 rounded-sm">
                    <h2 class="font-display text-2xl text-white mb-6">Order History</h2>
                    <table class="w-full text-left text-sm">
                        <thead class="text-gray-500 font-mono text-xs uppercase tracking-widest border-b border-gray-800">
                            <tr>
                                <th class="pb-4">Order</th>
                                <th class="pb-4">Date</th>
                                <th class="pb-4">Total</th>
                                <th class="pb-4">Status</th>
                                <th class="pb-4"></th>
                            </tr>
                        </thead>
                        <tbody class="text-gray-300">
                            <tr class="border-b border-gray-800">
                                <td class="py-4 font-mono">#ORD-091</td>
                                <td class="py-4">Yesterday</td>
                                <td class="py-4">$355.00</td>
                                <td class="py-4 text-success">Shipped</td>
                                <td class="py-4 text-right"><a href="order-detail.html" class="text-accent hover:text-white transition-colors">View</a></td>
                            </tr>
                            <tr>
                                <td class="py-4 font-mono">#ORD-085</td>
                                <td class="py-4">Sep 12, 2025</td>
                                <td class="py-4">$180.00</td>
                                <td class="py-4 text-success">Delivered</td>
                                <td class="py-4 text-right"><a href="order-detail.html" class="text-accent hover:text-white transition-colors">View</a></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
''',
    'user/profile.html': '''
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="md:col-span-1">
                <nav class="flex flex-col gap-2 bg-gray-900 border border-gray-800 p-4 rounded-sm">
                    <a href="dashboard.html" class="py-3 px-4 text-gray-400 hover:text-white font-mono text-xs uppercase tracking-widest transition-colors">Dashboard</a>
                    <a href="orders.html" class="py-3 px-4 text-gray-400 hover:text-white font-mono text-xs uppercase tracking-widest transition-colors">Orders</a>
                    <a href="wishlist.html" class="py-3 px-4 text-gray-400 hover:text-white font-mono text-xs uppercase tracking-widest transition-colors">Wishlist</a>
                    <a href="profile.html" class="py-3 px-4 bg-gray-800 text-accent font-mono text-xs uppercase tracking-widest">Profile</a>
                </nav>
            </div>
            <div class="md:col-span-3">
                <div class="bg-gray-900 border border-gray-800 p-8 rounded-sm max-w-2xl">
                    <h2 class="font-display text-2xl text-white mb-6">Personal Information</h2>
                    <form class="flex flex-col gap-6">
                        <div class="grid grid-cols-2 gap-6">
                            <div class="flex flex-col gap-2">
                                <label class="font-mono text-xs uppercase tracking-widest text-gray-500">First Name</label>
                                <input type="text" value="Michael" class="bg-transparent border-b border-gray-700 py-2 text-white focus:outline-none focus:border-accent">
                            </div>
                            <div class="flex flex-col gap-2">
                                <label class="font-mono text-xs uppercase tracking-widest text-gray-500">Last Name</label>
                                <input type="text" value="Chen" class="bg-transparent border-b border-gray-700 py-2 text-white focus:outline-none focus:border-accent">
                            </div>
                        </div>
                        <div class="flex flex-col gap-2">
                            <label class="font-mono text-xs uppercase tracking-widest text-gray-500">Email Address</label>
                            <input type="email" value="m.chen@example.com" class="bg-transparent border-b border-gray-700 py-2 text-white focus:outline-none focus:border-accent">
                        </div>
                        <button type="button" class="w-fit bg-white text-black px-8 py-3 mt-4 font-mono text-sm uppercase tracking-widest hover:bg-accent transition-colors">Save Changes</button>
                    </form>
                </div>
            </div>
        </div>
''',
    'user/wishlist.html': '''
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="md:col-span-1">
                <nav class="flex flex-col gap-2 bg-gray-900 border border-gray-800 p-4 rounded-sm">
                    <a href="dashboard.html" class="py-3 px-4 text-gray-400 hover:text-white font-mono text-xs uppercase tracking-widest transition-colors">Dashboard</a>
                    <a href="orders.html" class="py-3 px-4 text-gray-400 hover:text-white font-mono text-xs uppercase tracking-widest transition-colors">Orders</a>
                    <a href="wishlist.html" class="py-3 px-4 bg-gray-800 text-accent font-mono text-xs uppercase tracking-widest">Wishlist</a>
                    <a href="profile.html" class="py-3 px-4 text-gray-400 hover:text-white font-mono text-xs uppercase tracking-widest transition-colors">Profile</a>
                </nav>
            </div>
            <div class="md:col-span-3">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    <!-- Wishlist Item -->
                    <div class="bg-gray-900 border border-gray-800 p-4 rounded-sm relative group">
                        <button class="absolute top-6 right-6 text-gray-500 hover:text-error transition-colors">✕</button>
                        <div class="w-full aspect-[3/4] bg-gray-800 mb-4"></div>
                        <h4 class="font-display text-white mb-1">Structured Trench</h4>
                        <p class="font-mono text-accent text-sm mb-4">$420.00</p>
                        <button class="w-full py-2 border border-gray-700 text-white font-mono text-xs uppercase tracking-widest hover:border-accent hover:text-accent transition-colors">Move to Cart</button>
                    </div>
                </div>
            </div>
        </div>
'''
}

pattern = re.compile(r'<div class="content opacity-0 animate-fade-in-up">\s*<p class="text-gray-400">[^<]+Complete implementation[^<]+</p>\s*</div>')

for rel_path, replacement_html in replacements.items():
    file_path = os.path.join(base_dir, rel_path)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the boilerplate block
        new_content = pattern.sub(replacement_html, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {rel_path}")
    else:
        print(f"Not found: {file_path}")
