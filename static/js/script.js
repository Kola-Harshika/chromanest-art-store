/**
 * CHROMANEST - Modern Art Store E-Commerce
 * Vanilla JavaScript Core Engine
 * Handles State, LocalStorage (Cart & Wishlist), Catalog Discovery, Search & Filtering
 */

// -----------------------------------------------------------------------------
// 1. PRODUCT CATALOG DATA
// -----------------------------------------------------------------------------
let ART_CATALOG = [
  // --- PAINTINGS ---
  {
    id: "paint-01",
    title: "Ethereal Whispers",
    category: "Paintings",
    price: 280,
    originalPrice: 320,
    rating: 4.9,
    reviewsCount: 24,
    badge: "Curator's Pick",
    image: "/static/images/ethereal-whispers.jpg",
    medium: "Oil & 24K Gold Leaf on Belgian Linen",
    dimensions: "24 × 36 in (60 × 90 cm)",
    description: "An evocative exploration of quiet twilight horizons. Layered glazes of amethyst, soft blush, and hand-applied 24K gold leaf reflect changing room light throughout the day, evoking serene stillness.",
    details: [
      "Original 1-of-1 studio creation",
      "Finished with museum-grade protective UV varnish",
      "Includes signed Certificate of Authenticity",
      "Ready to hang with custom solid oak floater frame"
    ],
    inStock: true
  },
  {
    id: "paint-02",
    title: "Golden Horizon",
    category: "Paintings",
    price: 340,
    originalPrice: 380,
    rating: 5.0,
    reviewsCount: 19,
    badge: "Bestseller",
    image: "/static/images/golden-horizon.jpg",
    medium: "Textured Heavy Acrylic & Gold Leaf on Gallery Canvas",
    dimensions: "30 × 40 in (76 × 101 cm)",
    description: "Rich sculptural impasto strokes capture the warmth of the setting sun over rugged earthen landscape silhouettes. The tactile texture creates depth and dynamic shadows.",
    details: [
      "Heavy impasto palette knife technique",
      "Signature on lower right & reverse",
      "Includes Certificate of Authenticity",
      "Shipped in heavy-duty reinforced wooden crate"
    ],
    inStock: true
  },
  {
    id: "paint-03",
    title: "Serenade in Indigo",
    category: "Paintings",
    price: 220,
    originalPrice: null,
    rating: 4.8,
    reviewsCount: 15,
    badge: "New Release",
    image: "/static/images/serenade-indigo.jpg",
    medium: "Deep Mineral Pigment Wash on 640gsm Cold-Press Paper",
    dimensions: "20 × 28 in (50 × 70 cm)",
    description: "Hypnotic layers of lapis lazuli and indigo wash fluidly into soft mist. The organic crystallization of pure raw pigments creates a celestial meditation on paper.",
    details: [
      "Hand-deckled archival cotton rag paper",
      "Mounted behind anti-reflective museum glass",
      "Includes Certificate of Authenticity",
      "Signed and dated by the artist"
    ],
    inStock: true
  },
  {
    id: "paint-04",
    title: "Wild Botanical Bloom",
    category: "Paintings",
    price: 310,
    originalPrice: 350,
    rating: 5.0,
    reviewsCount: 18,
    badge: "Limited Release",
    image: "/static/images/wild-botanical-bloom.jpg",
    medium: "Oil & Botanical Glazes on Heavy Belgian Canvas",
    dimensions: "28 × 36 in (70 × 90 cm)",
    description: "A lush, painterly floral masterpiece featuring soft blush peonies, garden roses, and eucalyptus sprigs emerging from deep moody forest tones with rich impasto textures.",
    details: [
      "Original 1-of-1 studio floral composition",
      "Finished with protective museum satin varnish",
      "Includes signed Certificate of Authenticity",
      "Ready to hang in bespoke natural walnut floater frame"
    ],
    inStock: true
  },

  // --- RESIN ART ---
  {
    id: "resin-01",
    title: "Oceanic Geode Flow",
    category: "Resin Art",
    price: 195,
    originalPrice: 230,
    rating: 4.9,
    reviewsCount: 31,
    badge: "Bestseller",
    image: "/static/images/oceanic-geode.jpg",
    medium: "Multi-Layer Crystal Epoxy Resin, Real Quartz & Sea Pigments",
    dimensions: "20 × 20 in (50 × 50 cm)",
    description: "Translucent aquatic depths blended with shimmering mica swirls and embedded natural raw quartz points. Captures the eternal dance between sea foam and coastal reef.",
    details: [
      "High-gloss heat and scratch resistant topcoat",
      "Natural raw crushed quartz inclusions",
      "Solid birch wood substrate foundation",
      "Includes Certificate of Authenticity"
    ],
    inStock: true
  },
  {
    id: "resin-02",
    title: "Emerald Nebula Tray",
    category: "Resin Art",
    price: 145,
    originalPrice: null,
    rating: 4.9,
    reviewsCount: 18,
    badge: "Handcrafted",
    image: "/static/images/emerald-nebula.jpg",
    medium: "Hand-Poured Artisan Resin with Brushed Brass Handles",
    dimensions: "16 × 12 in (40 × 30 cm)",
    description: "A functional art centerpiece featuring deep emerald green pigment currents interlaced with gold glitter veining and solid brushed brass hardware.",
    details: [
      "Food-safe, scratch-resistant cured resin",
      "Heavy brushed solid brass handles",
      "Velvet padded bottom to protect furniture",
      "Care instructions included"
    ],
    inStock: true
  },
  {
    id: "resin-03",
    title: "Celestial Pearl Coasters",
    category: "Resin Art",
    price: 65,
    originalPrice: 75,
    rating: 4.7,
    reviewsCount: 42,
    badge: "Set of 4",
    image: "/static/images/celestial-pearl.jpg",
    medium: "Mother-of-Pearl Inlay & Lavender Epoxy Resin Set",
    dimensions: "4.5 in diameter (11.5 cm) each",
    description: "A luxurious 4-piece coaster suite infused with iridescent shell fragments, subtle lavender mineral clouds, and hand-gilded gold leaf edges.",
    details: [
      "Set of 4 individual coasters",
      "Heat-resistant up to 90°C (194°F)",
      "Hand-painted metallic gilded rim",
      "Gift-ready signature CHROMANEST linen box"
    ],
    inStock: true
  },

  // --- WALL ART ---
  {
    id: "wall-01",
    title: "Textured Terracotta Arcs",
    category: "Wall Art",
    price: 240,
    originalPrice: 280,
    rating: 5.0,
    reviewsCount: 27,
    badge: "Trending",
    image: "/static/images/textured-terracotta.jpg",
    medium: "3D Plaster & Mineral Earth Pigments on Reinforced Panel",
    dimensions: "24 × 32 in (60 × 80 cm)",
    description: "Architectural minimalism meets Mediterranean warmth. Rhythmic raised concentric arcs create captivating three-dimensional shadows across minimalist living spaces.",
    details: [
      "Sculpted dimensional plaster relief",
      "Natural organic matte finish",
      "Integrated heavy-duty hanging hardware",
      "Signed on reverse with edition stamp"
    ],
    inStock: true
  },
  {
    id: "wall-02",
    title: "Monochrome Rhythm",
    category: "Wall Art",
    price: 210,
    originalPrice: null,
    rating: 4.8,
    reviewsCount: 14,
    badge: "Minimalist",
    image: "/static/images/monochrome-rhythm.jpg",
    medium: "Geometric Ash Wood Slats & Blackened Mineral Canvas",
    dimensions: "28 × 28 in (70 × 70 cm)",
    description: "A study in balance, symmetry, and negative space. Hand-finished charred ash wood segments intersect on a textured linen backboard.",
    details: [
      "Solid sustainable kiln-dried ash wood",
      "Matte soot pigment wash",
      "Ultra-modern frameless aesthetic",
      "Includes mounting template"
    ],
    inStock: true
  },
  {
    id: "wall-03",
    title: "Gilded Botanical Relief",
    category: "Wall Art",
    price: 310,
    originalPrice: 350,
    rating: 4.9,
    reviewsCount: 19,
    badge: "Limited Edition",
    image: "/static/images/gilded-botanical.jpg",
    medium: "Hand-Carved Bas-Relief with Antique Gold Leaf Patina",
    dimensions: "22 × 34 in (56 × 86 cm)",
    description: "Inspired by pressed heritage ferns and ancient herbal manuscripts. Delicate leaf veins are hand-carved in high relief and finished in aged gold patina.",
    details: [
      "Hand-carved casting compound",
      "Distressed antique metallic leafing",
      "Encased in slim satin walnut shadowbox",
      "Certificate of Authenticity attached"
    ],
    inStock: true
  },

  // --- HANDMADE ---
  {
    id: "hand-01",
    title: "Sculpted Clay Muse Vase",
    category: "Handmade",
    price: 135,
    originalPrice: 155,
    rating: 4.9,
    reviewsCount: 38,
    badge: "Studio Exclusive",
    image: "/static/images/sculpted-clay-vase.jpg",
    medium: "Wheel-Thrown Stoneware with Matte Raw Glaze",
    dimensions: "11 × 7 in (28 × 18 cm)",
    description: "Hand-sculpted organic silhouette inspired by classical Greek amphorae and modern brutalism. Each vessel bears subtle finger ridges from the potter's wheel.",
    details: [
      "100% waterproof glazed interior",
      "Tactile raw sand exterior texture",
      "Individually hand-thrown in studio",
      "Artist studio stamp on base"
    ],
    inStock: true
  },
  {
    id: "hand-02",
    title: "Artisan Ceramic Vessel",
    category: "Handmade",
    price: 110,
    originalPrice: null,
    rating: 4.7,
    reviewsCount: 22,
    badge: "Original",
    image: "/static/images/artisan-ceramic-vessel.jpg",
    medium: "Matte Charcoal Studio Stoneware with Speckled Lip",
    dimensions: "9 × 6 in (23 × 15 cm)",
    description: "A striking minimalist statement vessel with earthy charcoal tones and an asymmetrical organic mouth, celebrating the wabi-sabi beauty of imperfection.",
    details: [
      "High-fire reduction stoneware",
      "Handmade in small batches",
      "Sturdy heavy-weight base",
      "Care booklet included"
    ],
    inStock: true
  },
  {
    id: "hand-03",
    title: "Handwoven Dune Tapestry",
    category: "Handmade",
    price: 175,
    originalPrice: 200,
    rating: 5.0,
    reviewsCount: 16,
    badge: "Hand-Loomed",
    image: "/static/images/woven-tapestry-dune.jpg",
    medium: "Organic Merino Wool, Raw Flax Linen & Brass Bar",
    dimensions: "18 × 36 in (45 × 90 cm)",
    description: "Textured wall fiber art hand-loomed with undyed ethical wool and raw linen fibers. Inspired by shifting desert dunes and organic earthen topography.",
    details: [
      "Spun from 100% cruelty-free merino wool",
      "Suspended on solid natural brass rod",
      "Subtle fringed bottom drape",
      "Comes ready to hang"
    ],
    inStock: true
  },

  // --- ART PRINTS ---
  {
    id: "print-01",
    title: "Sunlit Olive Grove",
    category: "Art Prints",
    price: 75,
    originalPrice: 90,
    rating: 4.8,
    reviewsCount: 52,
    badge: "Archival Giclée",
    image: "/static/images/sunlit-olive-grove.jpg",
    medium: "Museum-Grade 310gsm 100% Cotton Rag Archival Giclée",
    dimensions: "18 × 24 in (45 × 60 cm)",
    description: "Dappled sunlight filtering through silvery Tuscan olive branches. Printed with 12-color archival pigment inks guaranteed to remain vibrant for over 100 years.",
    details: [
      "Hahnemühle Photo Rag paper",
      "12-color pigment Lucia PRO ink",
      "Hand-embossed CHROMANEST seal",
      "Shipped flat in protective acid-free sleeve"
    ],
    inStock: true
  },
  {
    id: "print-02",
    title: "Abstract Fluidity No. 4",
    category: "Art Prints",
    price: 85,
    originalPrice: null,
    rating: 4.9,
    reviewsCount: 29,
    badge: "Limited Edition / 100",
    image: "/static/images/abstract-fluidity.jpg",
    medium: "Hand-Numbered Fine Art Lithograph on Textured Velvet Paper",
    dimensions: "20 × 28 in (50 × 70 cm)",
    description: "A dynamic composition of flowing mauve, plum, and warm ochre shapes. Part of an exclusive numbered edition of only 100 prints worldwide.",
    details: [
      "Hand-numbered and pencil signed",
      "Certificate of Authenticity included",
      "Acid-free archival backing",
      "Fits standard gallery frames"
    ],
    inStock: true
  },
  {
    id: "print-03",
    title: "Midnight Flora Lithograph",
    category: "Art Prints",
    price: 65,
    originalPrice: 80,
    rating: 4.7,
    reviewsCount: 34,
    badge: "Popular",
    image: "/static/images/midnight-flora.jpg",
    medium: "Embossed Midnight Blue & Silver Ink Botanical Print",
    dimensions: "16 × 20 in (40 × 50 cm)",
    description: "Botanical elegance captured in nocturnal tones. Silver metallic botanical silhouettes shimmer delicately over a deep navy velvety background.",
    details: [
      "Double-hit metallic silver ink print",
      "Deckled bottom edge",
      "Archival matte paper",
      "Includes hanging guidelines"
    ],
    inStock: true
  },

  // --- CUSTOMIZED GIFTS ---
  {
    id: "gift-01",
    title: "Bespoke Couple Watercolor",
    category: "Customized Gifts",
    price: 185,
    originalPrice: 220,
    rating: 5.0,
    reviewsCount: 64,
    badge: "Custom Commission",
    image: "/static/images/custom-watercolor-gift.jpg",
    medium: "Custom Hand-Painted Watercolor from Your Reference Photo",
    dimensions: "12 × 16 in (30 × 40 cm)",
    description: "Transform your favorite memory, wedding photo, or family moment into a luminous, expressive watercolor portrait handcrafted by our master illustrators.",
    details: [
      "Custom painted directly from your photo",
      "Digital preview & approval before final varnishing",
      "Includes personalized calligraphy inscription",
      "Gift-boxed with luxury satin ribbon"
    ],
    inStock: true
  },
  {
    id: "gift-02",
    title: "Personalized Resin Plaque",
    category: "Customized Gifts",
    price: 125,
    originalPrice: null,
    rating: 4.9,
    reviewsCount: 47,
    badge: "Personalized",
    image: "/static/images/custom-resin-plaque.jpg",
    medium: "Hand-Poured Botanical Resin with Custom Gilded Inscription",
    dimensions: "10 × 10 in (25 × 25 cm)",
    description: "Real pressed flowers, gold flakes, and crystal-clear resin cast around your custom names, anniversary dates, or meaningful vows.",
    details: [
      "Custom laser-engraved or gilded script",
      "Preserved organic botanicals",
      "Includes solid wood tabletop display easel",
      "Turnaround time: 5-7 business days"
    ],
    inStock: true
  }
];

// -----------------------------------------------------------------------------
// 2. STATE & LOCALSTORAGE MANAGEMENT
// -----------------------------------------------------------------------------
const STORAGE_KEYS = {
  CART: 'chromanest_cart',
  WISHLIST: 'chromanest_wishlist'
};

function getCart() {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.CART);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    console.error("Cart retrieval error:", e);
    return [];
  }
}

function saveCart(cart) {
  try {
    localStorage.setItem(STORAGE_KEYS.CART, JSON.stringify(cart));
    updateBadges();
  } catch (e) {
    console.error("Cart save error:", e);
  }
}

function addToCart(productId, quantity = 1) {
  const product = ART_CATALOG.find(p => p.id === productId);
  if (!product) return;

  let cart = getCart();
  const existingIndex = cart.findIndex(item => item.id === productId);

  if (existingIndex > -1) {
    cart[existingIndex].quantity += quantity;
  } else {
    cart.push({
      id: product.id,
      title: product.title,
      price: product.price,
      image: product.image,
      category: product.category,
      medium: product.medium,
      quantity: quantity
    });
  }

  saveCart(cart);
  showToast("Added to Cart", `"${product.title}" is now in your shopping bag.`, "success");
}

function removeFromCart(productId) {
  let cart = getCart();
  const removedItem = cart.find(item => item.id === productId);
  cart = cart.filter(item => item.id !== productId);
  saveCart(cart);
  if (removedItem) {
    showToast("Item Removed", `"${removedItem.title}" was removed from your bag.`, "info");
  }
}

function updateCartQuantity(productId, quantity) {
  let cart = getCart();
  const item = cart.find(item => item.id === productId);
  if (item) {
    item.quantity = Math.max(1, parseInt(quantity) || 1);
    saveCart(cart);
  }
}

function getWishlist() {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.WISHLIST);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    console.error("Wishlist retrieval error:", e);
    return [];
  }
}

function saveWishlist(wishlist) {
  try {
    localStorage.setItem(STORAGE_KEYS.WISHLIST, JSON.stringify(wishlist));
    updateBadges();
    syncWishlistButtons();
  } catch (e) {
    console.error("Wishlist save error:", e);
  }
}

function toggleWishlist(productId) {
  let wishlist = getWishlist();
  const product = ART_CATALOG.find(p => p.id === productId);
  const index = wishlist.indexOf(productId);

  if (index > -1) {
    wishlist.splice(index, 1);
    saveWishlist(wishlist);
    showToast("Removed from Wishlist", `"${product ? product.title : 'Artwork'}" removed from saved pieces.`, "info");
  } else {
    wishlist.push(productId);
    saveWishlist(wishlist);
    showToast("Saved to Wishlist", `"${product ? product.title : 'Artwork'}" added to your curated list.`, "success");
  }
}

function isInWishlist(productId) {
  return getWishlist().includes(productId);
}

// -----------------------------------------------------------------------------
// 3. BADGES & UI SYNCHRONIZATION
// -----------------------------------------------------------------------------
function updateBadges() {
  const cart = getCart();
  const totalCartCount = cart.reduce((sum, item) => sum + item.quantity, 0);
  const wishlist = getWishlist();

  document.querySelectorAll('.cart-count-badge').forEach(el => {
    el.textContent = totalCartCount;
    el.style.display = totalCartCount > 0 ? 'flex' : 'none';
  });

  document.querySelectorAll('.wishlist-count-badge').forEach(el => {
    el.textContent = wishlist.length;
    el.style.display = wishlist.length > 0 ? 'flex' : 'none';
  });
}

function syncWishlistButtons() {
  const wishlist = getWishlist();
  document.querySelectorAll('[data-wishlist-id]').forEach(btn => {
    const id = btn.getAttribute('data-wishlist-id');
    const isSaved = wishlist.includes(id);
    btn.classList.toggle('active', isSaved);
    const icon = btn.querySelector('i');
    if (icon) {
      icon.className = isSaved ? 'fas fa-heart' : 'far fa-heart';
    }
  });
}

// -----------------------------------------------------------------------------
// 4. TOAST NOTIFICATION SYSTEM
// -----------------------------------------------------------------------------
function showToast(title, message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;

  const iconMap = {
    success: 'fas fa-check-circle',
    info: 'fas fa-info-circle',
    error: 'fas fa-exclamation-circle'
  };

  toast.innerHTML = `
    <div class="toast-icon">
      <i class="${iconMap[type] || iconMap.success}"></i>
    </div>
    <div class="toast-message">
      <div class="toast-title">${title}</div>
      <div class="toast-text">${message}</div>
    </div>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// -----------------------------------------------------------------------------
// 5. WISHLIST DRAWER
// -----------------------------------------------------------------------------
function initWishlistDrawer() {
  const drawerOverlay = document.getElementById('wishlist-drawer-overlay');
  const drawerPanel = document.getElementById('wishlist-drawer-panel');
  const openButtons = document.querySelectorAll('.open-wishlist-trigger');
  const closeButton = document.getElementById('close-wishlist-drawer');
  const drawerContent = document.getElementById('wishlist-drawer-items');

  if (!drawerOverlay || !drawerPanel) return;

  function renderWishlistDrawer() {
    const wishlistIds = getWishlist();
    if (!drawerContent) return;

    if (wishlistIds.length === 0) {
      drawerContent.innerHTML = `
        <div class="empty-state" style="padding: 3rem 1rem;">
          <div class="empty-state-icon"><i class="far fa-heart"></i></div>
          <h3>Your wishlist is empty</h3>
          <p>Explore our gallery and save artworks you love.</p>
          <a href="/shop" class="btn btn-primary btn-sm" style="margin-top: 1rem;">Browse Collection</a>
        </div>
      `;
      return;
    }

    const items = ART_CATALOG.filter(p => wishlistIds.includes(p.id));
    drawerContent.innerHTML = items.map(item => `
      <div class="wishlist-item-card">
        <div class="wishlist-item-img">
          <img src="${item.image}" alt="${item.title}" onerror="this.src='/static/images/hero-art.jpg'">
        </div>
        <div class="wishlist-item-details">
          <h4>${item.title}</h4>
          <p>$${item.price}</p>
          <div style="display: flex; gap: 0.5rem; margin-top: 0.4rem;">
            <button class="btn btn-primary btn-sm" onclick="moveWishlistToCart('${item.id}')" style="padding: 0.35rem 0.75rem; font-size: 0.75rem;">
              <i class="fas fa-shopping-bag"></i> Move to Cart
            </button>
            <button class="btn btn-secondary btn-sm" onclick="toggleWishlist('${item.id}'); renderWishlistDrawer();" style="padding: 0.35rem 0.6rem; font-size: 0.75rem; color: #E63946;">
              <i class="fas fa-trash-alt"></i>
            </button>
          </div>
        </div>
      </div>
    `).join('');
  }

  window.renderWishlistDrawer = renderWishlistDrawer;
  window.moveWishlistToCart = function(productId) {
    addToCart(productId, 1);
    toggleWishlist(productId);
    renderWishlistDrawer();
  };

  function openDrawer(e) {
    if (e) e.preventDefault();
    renderWishlistDrawer();
    drawerOverlay.classList.add('active');
    drawerPanel.classList.add('active');
  }

  function closeDrawer() {
    drawerOverlay.classList.remove('active');
    drawerPanel.classList.remove('active');
  }

  openButtons.forEach(btn => btn.addEventListener('click', openDrawer));
  if (closeButton) closeButton.addEventListener('click', closeDrawer);
  drawerOverlay.addEventListener('click', closeDrawer);
}

// -----------------------------------------------------------------------------
// 6. SHOP CATALOG PAGE (FILTERING, SEARCH & SORT)
// -----------------------------------------------------------------------------
function initShopPage() {
  const gridContainer = document.getElementById('shop-products-grid');
  if (!gridContainer) return;

  const searchInput = document.getElementById('shop-search-input');
  const sortSelect = document.getElementById('shop-sort-select');
  const pillsContainer = document.getElementById('category-pills');
  const countDisplay = document.getElementById('products-count-display');
  const clearFiltersBtn = document.getElementById('clear-filters-btn');

  // URL parameters state
  const urlParams = new URLSearchParams(window.location.search);
  let currentCategory = urlParams.get('category') || 'All';
  let currentSearch = urlParams.get('search') || '';
  let currentSort = 'featured';

  if (searchInput && currentSearch) {
    searchInput.value = currentSearch;
  }

  function filterAndRender() {
    let filtered = [...ART_CATALOG];

    // Filter by Category
    if (currentCategory !== 'All') {
      filtered = filtered.filter(item => item.category.toLowerCase() === currentCategory.toLowerCase());
    }

    // Filter by Search Query
    if (currentSearch.trim() !== '') {
      const q = currentSearch.toLowerCase().trim();
      filtered = filtered.filter(item => 
        item.title.toLowerCase().includes(q) ||
        item.category.toLowerCase().includes(q) ||
        item.medium.toLowerCase().includes(q) ||
        item.description.toLowerCase().includes(q)
      );
    }

    // Sorting
    if (currentSort === 'price-low') {
      filtered.sort((a, b) => a.price - b.price);
    } else if (currentSort === 'price-high') {
      filtered.sort((a, b) => b.price - a.price);
    } else if (currentSort === 'rating') {
      filtered.sort((a, b) => b.rating - a.rating);
    } else if (currentSort === 'name-asc') {
      filtered.sort((a, b) => a.title.localeCompare(b.title));
    }

    // Update Counts & Pill states
    if (countDisplay) {
      countDisplay.textContent = `Showing ${filtered.length} ${filtered.length === 1 ? 'artwork' : 'artworks'}`;
    }

    document.querySelectorAll('.category-pill').forEach(pill => {
      const cat = pill.getAttribute('data-category');
      pill.classList.toggle('active', cat.toLowerCase() === currentCategory.toLowerCase());
    });

    if (filtered.length === 0) {
      gridContainer.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1;">
          <div class="empty-state-icon"><i class="fas fa-search"></i></div>
          <h3>No Artworks Found</h3>
          <p>We couldn't find any artworks matching "${currentSearch || currentCategory}".</p>
          <button class="btn btn-primary btn-sm" onclick="resetShopFilters()" style="margin-top: 1rem;">Reset Filters</button>
        </div>
      `;
      return;
    }

    // Render Product Cards
    gridContainer.innerHTML = filtered.map(item => createProductCardHtml(item)).join('');
    syncWishlistButtons();
  }

  window.resetShopFilters = function() {
    currentCategory = 'All';
    currentSearch = '';
    currentSort = 'featured';
    if (searchInput) searchInput.value = '';
    if (sortSelect) sortSelect.value = 'featured';
    filterAndRender();
  };

  // Event Listeners
  if (pillsContainer) {
    pillsContainer.addEventListener('click', (e) => {
      const pill = e.target.closest('.category-pill');
      if (!pill) return;
      currentCategory = pill.getAttribute('data-category');
      filterAndRender();
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      currentSearch = e.target.value;
      filterAndRender();
    });
  }

  if (sortSelect) {
    sortSelect.addEventListener('change', (e) => {
      currentSort = e.target.value;
      filterAndRender();
    });
  }

  if (clearFiltersBtn) {
    clearFiltersBtn.addEventListener('click', (e) => {
      e.preventDefault();
      window.resetShopFilters();
    });
  }

  // Initial render
  filterAndRender();
}

function createProductCardHtml(item) {
  const isSaved = isInWishlist(item.id);
  const oldPriceHtml = item.originalPrice ? `<span class="product-price-old">$${item.originalPrice}</span>` : '';
  const badgeHtml = item.badge ? `<span class="product-badge ${item.badge === 'Bestseller' ? 'gold' : ''}">${item.badge}</span>` : '';

  return `
    <div class="product-card" data-product-id="${item.id}">
      <div class="product-image-container">
        ${badgeHtml}
        <button class="product-wishlist-btn ${isSaved ? 'active' : ''}" data-wishlist-id="${item.id}" onclick="toggleWishlist('${item.id}')" aria-label="Save to Wishlist">
          <i class="${isSaved ? 'fas' : 'far'} fa-heart"></i>
        </button>
        <a href="/product?id=${item.id}">
          <img src="${item.image}" alt="${item.title}" loading="lazy" onerror="this.src='/static/images/hero-art.jpg'">
        </a>
        <div class="product-quick-actions">
          <a href="/product?id=${item.id}" class="btn btn-secondary btn-sm">Details</a>
          <button class="btn btn-primary btn-sm" onclick="addToCart('${item.id}', 1)">+ Add to Bag</button>
        </div>
      </div>
      <div class="product-info">
        <div class="product-category">${item.category}</div>
        <h3 class="product-title"><a href="/product?id=${item.id}">${item.title}</a></h3>
        <div class="product-medium">${item.medium}</div>
        <div class="product-meta-row">
          <div class="product-price">$${item.price} ${oldPriceHtml}</div>
          <div class="product-rating">
            <i class="fas fa-star"></i>
            <span>${item.rating} (${item.reviewsCount})</span>
          </div>
        </div>
      </div>
    </div>
  `;
}

// -----------------------------------------------------------------------------
// 7. PRODUCT DETAILS PAGE
// -----------------------------------------------------------------------------
function initProductPage() {
  const container = document.getElementById('product-detail-view');
  if (!container) return;

  const urlParams = new URLSearchParams(window.location.search);
  const productId = urlParams.get('id') || 'paint-01';
  const product = ART_CATALOG.find(p => p.id === productId) || ART_CATALOG[0];

  document.title = `${product.title} — CHROMANEST Modern Art Store`;

  // Render Product Page Content
  const oldPriceHtml = product.originalPrice ? `<span class="product-price-old" style="font-size: 1.2rem; text-decoration: line-through; color: var(--text-muted);">$${product.originalPrice}</span>` : '';
  const isSaved = isInWishlist(product.id);

  container.innerHTML = `
    <nav class="breadcrumb">
      <a href="/">Home</a> <span>/</span>
      <a href="/shop">Shop</a> <span>/</span>
      <a href="/shop?category=${encodeURIComponent(product.category)}">${product.category}</a> <span>/</span>
      <span>${product.title}</span>
    </nav>

    <div class="product-detail-layout">
      <!-- Gallery Column -->
      <div class="product-gallery">
        <div class="main-image-frame">
          <img id="detail-main-img" src="${product.image}" alt="${product.title}" onerror="this.src='/static/images/hero-art.jpg'">
        </div>
        <div class="product-thumbnails">
          <div class="thumb-item active" onclick="swapDetailImage(this, '${product.image}')">
            <img src="${product.image}" alt="${product.title}">
          </div>
          <div class="thumb-item" onclick="swapDetailImage(this, '/static/images/hero-art.jpg')">
            <img src="/static/images/hero-art.jpg" alt="Gallery View">
          </div>
          <div class="thumb-item" onclick="swapDetailImage(this, '/static/images/about-artist.jpg')">
            <img src="/static/images/about-artist.jpg" alt="Studio View">
          </div>
        </div>
      </div>

      <!-- Info Column -->
      <div class="product-detail-info">
        <div class="product-detail-category">${product.category}</div>
        <h1 class="product-detail-title">${product.title}</h1>
        
        <div class="product-detail-meta">
          <div class="product-rating" style="font-size: 0.95rem;">
            <i class="fas fa-star"></i>
            <span>${product.rating} (from ${product.reviewsCount} art collector reviews)</span>
          </div>
          <div class="stock-status">
            <span class="stock-dot"></span> In Stock & Ready to Dispatch
          </div>
        </div>

        <div class="product-detail-price">
          $${product.price} ${oldPriceHtml}
        </div>

        <p class="product-detail-desc">${product.description}</p>

        <div class="artwork-specs-list">
          <div class="spec-item">
            <strong>Medium / Materials</strong>
            ${product.medium}
          </div>
          <div class="spec-item">
            <strong>Dimensions</strong>
            ${product.dimensions}
          </div>
          <div class="spec-item">
            <strong>Authenticity</strong>
            Signed & Certified
          </div>
          <div class="spec-item">
            <strong>Shipping Guarantee</strong>
            Insured Worldwide Delivery
          </div>
        </div>

        <!-- Quantity & Add to Cart -->
        <div class="action-box">
          <div class="quantity-selector">
            <button class="qty-btn" onclick="stepQty(-1)" aria-label="Decrease quantity"><i class="fas fa-minus"></i></button>
            <input type="number" id="detail-quantity" class="qty-input" value="1" min="1" max="10" readonly>
            <button class="qty-btn" onclick="stepQty(1)" aria-label="Increase quantity"><i class="fas fa-plus"></i></button>
          </div>
          <div class="product-detail-actions">
            <button class="btn btn-primary btn-lg" style="flex: 2;" onclick="addDetailToCart('${product.id}')">
              <i class="fas fa-shopping-bag"></i> Add to Cart
            </button>
            <button class="btn btn-secondary btn-icon-only" style="width: 52px; height: 52px;" data-wishlist-id="${product.id}" onclick="toggleWishlist('${product.id}')" aria-label="Add to Wishlist">
              <i class="${isSaved ? 'fas' : 'far'} fa-heart"></i>
            </button>
          </div>
        </div>

        <!-- Tabs -->
        <div class="product-tabs-container">
          <div class="tabs-header">
            <button class="tab-btn active" onclick="openTab(event, 'tab-story')">Artwork Story</button>
            <button class="tab-btn" onclick="openTab(event, 'tab-specs')">Specifications & Care</button>
            <button class="tab-btn" onclick="openTab(event, 'tab-shipping')">Shipping & Authenticity</button>
          </div>

          <div id="tab-story" class="tab-content active">
            <p>${product.description}</p>
            <p style="margin-top: 1rem;">Created in the CHROMANEST Atelier using bespoke hand-mixed mineral pigments, natural binders, and artisan finishes. Each composition is born from meditative studies of light and natural architectural rhythm.</p>
          </div>

          <div id="tab-specs" class="tab-content">
            <ul style="list-style: disc; padding-left: 1.2rem; display: flex; flex-direction: column; gap: 0.6rem;">
              ${product.details.map(d => `<li>${d}</li>`).join('')}
              <li>Care: Dust gently with a clean dry microfiber cloth. Keep out of extreme humidity and direct harsh sun exposure.</li>
            </ul>
          </div>

          <div id="tab-shipping" class="tab-content">
            <p>Every artwork is inspected, museum-wrapped in acid-free glassine paper, surrounded by custom impact-absorbing foam, and packaged in double-walled reinforced wooden or rigid crates.</p>
            <p style="margin-top: 0.8rem;">Complimentary tracked and insured courier shipping on orders over $150. Returns accepted within 14 days of delivery.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Related Artworks Section -->
    <div style="margin-top: 6rem; padding-top: 4rem; border-top: 1px solid var(--border-color);">
      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
        <span class="section-tag">Curated Recommendations</span>
        <h2 class="section-title" style="font-size: 2rem;">You May Also Admire</h2>
      </div>
      <div class="products-grid" id="related-artworks-grid"></div>
    </div>
  `;

  // Render Related Artworks
  const relatedGrid = document.getElementById('related-artworks-grid');
  if (relatedGrid) {
    const related = ART_CATALOG.filter(p => p.id !== product.id && p.category === product.category).slice(0, 3);
    const fallback = ART_CATALOG.filter(p => p.id !== product.id && !related.includes(p)).slice(0, 3 - related.length);
    const combined = [...related, ...fallback].slice(0, 3);
    relatedGrid.innerHTML = combined.map(item => createProductCardHtml(item)).join('');
  }

  syncWishlistButtons();

  window.swapDetailImage = function(thumbElement, src) {
    document.querySelectorAll('.thumb-item').forEach(el => el.classList.remove('active'));
    thumbElement.classList.add('active');
    const mainImg = document.getElementById('detail-main-img');
    if (mainImg) mainImg.src = src;
  };

  window.stepQty = function(delta) {
    const input = document.getElementById('detail-quantity');
    if (!input) return;
    let val = parseInt(input.value) || 1;
    val = Math.max(1, Math.min(10, val + delta));
    input.value = val;
  };

  window.addDetailToCart = function(id) {
    const input = document.getElementById('detail-quantity');
    const qty = input ? parseInt(input.value) || 1 : 1;
    addToCart(id, qty);
  };

  window.openTab = function(evt, tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    evt.currentTarget.classList.add('active');
    const target = document.getElementById(tabId);
    if (target) target.classList.add('active');
  };
}

// -----------------------------------------------------------------------------
// 8. CART PAGE
// -----------------------------------------------------------------------------
function initCartPage() {
  const container = document.getElementById('cart-page-view');
  if (!container) return;

  let promoDiscount = 0; // percentage or fixed
  let activePromoCode = '';

  function renderCartView() {
    const cart = getCart();

    if (cart.length === 0) {
      container.innerHTML = `
        <div class="empty-state" style="margin: 4rem auto; max-width: 600px;">
          <div class="empty-state-icon"><i class="fas fa-shopping-bag"></i></div>
          <h2 style="font-size: 1.8rem; margin-bottom: 0.6rem;">Your Shopping Bag is Empty</h2>
          <p>Discover unique, original artworks and artisanal gifts handcrafted with passion.</p>
          <a href="/shop" class="btn btn-primary btn-lg" style="margin-top: 1.8rem;">Explore Collection</a>
        </div>
      `;
      return;
    }

    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const shipping = subtotal >= 150 ? 0 : 25;
    const discountAmount = promoDiscount > 0 ? (subtotal * promoDiscount) : 0;
    const tax = (subtotal - discountAmount) * 0.05;
    const total = subtotal - discountAmount + shipping + tax;

    container.innerHTML = `
      <div class="cart-layout">
        <!-- Cart Items List -->
        <div class="cart-items-card">
          <div style="display: flex; justify-content: space-between; align-items: baseline; padding-bottom: 1.2rem; border-bottom: 1px solid var(--border-color);">
            <h2 style="font-size: 1.6rem;">Artworks in Bag (${cart.reduce((s, i) => s + i.quantity, 0)})</h2>
            <a href="/shop" style="font-size: 0.88rem; color: var(--accent-lavender-dark); font-weight: 600;">+ Continue Shopping</a>
          </div>

          <div class="cart-items-list">
            ${cart.map(item => `
              <div class="cart-item-row" data-id="${item.id}">
                <div class="cart-item-img">
                  <img src="${item.image}" alt="${item.title}" onerror="this.src='/static/images/hero-art.jpg'">
                </div>
                <div>
                  <div class="cart-item-category">${item.category}</div>
                  <h4 class="cart-item-title"><a href="/product?id=${item.id}">${item.title}</a></h4>
                  <div style="font-size: 0.85rem; color: var(--text-muted);">$${item.price} each</div>
                </div>
                <div class="cart-item-price">$${item.price}</div>
                <div>
                  <div class="quantity-selector" style="height: 38px;">
                    <button class="qty-btn" onclick="modifyCartQty('${item.id}', -1)" aria-label="Decrease"><i class="fas fa-minus" style="font-size: 0.75rem;"></i></button>
                    <input type="number" class="qty-input" value="${item.quantity}" readonly style="width: 36px; font-size: 0.9rem;">
                    <button class="qty-btn" onclick="modifyCartQty('${item.id}', 1)" aria-label="Increase"><i class="fas fa-plus" style="font-size: 0.75rem;"></i></button>
                  </div>
                </div>
                <div class="cart-item-subtotal">$${(item.price * item.quantity).toFixed(2)}</div>
                <div>
                  <button class="cart-remove-btn" onclick="deleteCartItem('${item.id}')" title="Remove Item">
                    <i class="fas fa-trash-alt"></i>
                  </button>
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Order Summary Card -->
        <div class="order-summary-card">
          <h3 class="summary-title">Order Summary</h3>

          <div class="summary-row">
            <span>Subtotal</span>
            <span>$${subtotal.toFixed(2)}</span>
          </div>

          ${promoDiscount > 0 ? `
            <div class="summary-row" style="color: var(--accent-sage); font-weight: 600;">
              <span>Promo (${activePromoCode} - ${promoDiscount * 100}%)</span>
              <span>-$${discountAmount.toFixed(2)}</span>
            </div>
          ` : ''}

          <div class="summary-row">
            <span>Insured Courier Shipping</span>
            <span>${shipping === 0 ? '<strong style="color: var(--accent-sage);">FREE</strong>' : `$${shipping.toFixed(2)}`}</span>
          </div>

          <div class="summary-row">
            <span>Estimated Art Tax (5%)</span>
            <span>$${tax.toFixed(2)}</span>
          </div>

          <form class="promo-form" onsubmit="applyPromo(event)">
            <input type="text" id="promo-code-input" class="promo-input" placeholder="Promo code (e.g. ART10)" value="${activePromoCode}">
            <button type="submit" class="btn btn-secondary btn-sm">Apply</button>
          </form>

          <div class="summary-row total">
            <span>Estimated Total</span>
            <span>$${total.toFixed(2)}</span>
          </div>

          <button class="btn btn-primary btn-lg" style="width: 100%; margin-top: 1.5rem;" onclick="openCheckoutModal(${total.toFixed(2)})">
            <i class="fas fa-lock"></i> Secure Checkout
          </button>

          <div style="margin-top: 1.5rem; text-align: center; font-size: 0.8rem; color: var(--text-muted);">
            <i class="fas fa-shield-alt" style="color: var(--accent-lavender); margin-right: 4px;"></i> 256-Bit SSL Encrypted & Museum Transit Insurance Included
          </div>
        </div>
      </div>
    `;
  }

  window.modifyCartQty = function(id, delta) {
    let cart = getCart();
    const item = cart.find(i => i.id === id);
    if (item) {
      item.quantity = Math.max(1, item.quantity + delta);
      saveCart(cart);
      renderCartView();
    }
  };

  window.deleteCartItem = function(id) {
    removeFromCart(id);
    renderCartView();
  };

  window.applyPromo = function(e) {
    e.preventDefault();
    const input = document.getElementById('promo-code-input');
    const code = input ? input.value.trim().toUpperCase() : '';

    if (code === 'ART10' || code === 'CHROMANEST10') {
      promoDiscount = 0.10;
      activePromoCode = code;
      showToast("Promo Code Applied", "10% collector discount has been applied to your order.", "success");
      renderCartView();
    } else if (code === 'WELCOME20') {
      promoDiscount = 0.20;
      activePromoCode = code;
      showToast("Promo Code Applied", "20% welcome discount has been applied!", "success");
      renderCartView();
    } else {
      showToast("Invalid Promo Code", "Try using code 'ART10' for 10% off.", "error");
    }
  };

  renderCartView();
}

// -----------------------------------------------------------------------------
// 9. CHECKOUT SIMULATION / ROUTING
// -----------------------------------------------------------------------------
function openCheckoutModal(amount) {
  window.location.href = '/checkout';
}

// -----------------------------------------------------------------------------
// 10. COMMON UI (NAVBAR, FORMS, FAQ ACCORDION)
// -----------------------------------------------------------------------------
function initCommonUI() {
  // Mobile Nav Toggle
  const mobileToggle = document.querySelector('.mobile-toggle');
  const navMenu = document.querySelector('.nav-menu');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      mobileToggle.classList.toggle('active');
      navMenu.classList.toggle('active');
    });
  }

  // Header Scroll Shadow
  const header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 20);
    });
  }

  // FAQ Accordions
  document.querySelectorAll('.accordion-header').forEach(headerEl => {
    headerEl.addEventListener('click', () => {
      const item = headerEl.parentElement;
      const isActive = item.classList.contains('active');
      document.querySelectorAll('.accordion-item').forEach(other => other.classList.remove('active'));
      if (!isActive) {
        item.classList.add('active');
      }
    });
  });

  // Newsletter Forms
  document.querySelectorAll('.newsletter-form').forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = form.querySelector('input[type="email"]');
      if (input && input.value.includes('@')) {
        showToast("Subscribed to the Atelier Gazette", "Thank you for joining our private collector circle.", "success");
        input.value = '';
      } else {
        showToast("Invalid Email", "Please enter a valid email address.", "error");
      }
    });
  });

  // Contact Form
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('contact-name')?.value || 'Collector';
      showToast("Message Sent", `Thank you ${name}. Our gallery curator will get back to you within 24 hours.`, "success");
      contactForm.reset();
    });
  }

  // Wishlist buttons in static markup
  syncWishlistButtons();
  updateBadges();
}

// -----------------------------------------------------------------------------
// 11. INITIALIZATION ON DOM READY
// -----------------------------------------------------------------------------
async function syncCatalogFromApi() {
  try {
    const res = await fetch('/api/products');
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        ART_CATALOG = data.map(p => ({
          id: p.id,
          title: p.title,
          category: p.category,
          price: p.price,
          originalPrice: p.original_price,
          rating: p.rating || 5.0,
          reviewsCount: p.reviews_count || 0,
          badge: p.badge,
          image: p.image,
          medium: p.medium,
          dimensions: p.dimensions,
          description: p.description,
          details: p.details || [],
          inStock: p.in_stock === 1 || p.in_stock === true
        }));
      }
    }
  } catch (e) {
    // Fall back to pre-seeded local ART_CATALOG
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  initCommonUI();
  initWishlistDrawer();
  await syncCatalogFromApi();
  initShopPage();
  initProductPage();
  initCartPage();
});
