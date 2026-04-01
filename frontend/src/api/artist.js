export const getArtistStats = async () => {
  // Simulate network request
  await new Promise(resolve => setTimeout(resolve, 600))
  
  return {
    totalRevenue: '₹2,45,000',
    totalOrders: 142,
    catalogueViews: 12450,
    storyEngagement: '8.4%',
    revenueTrend: [12000, 18000, 22000, 26000, 31000, 42000, 48000],
    viewsTrend: [2000, 3200, 4100, 4900, 6200, 8100, 10200],
    months: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
  }
}
