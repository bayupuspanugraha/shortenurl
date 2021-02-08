using csharp.Models;
using Microsoft.EntityFrameworkCore;

namespace csharp.DB
{
    public class AppDbContext : DbContext
    {
        public DbSet<ShortenURLViewModel> ShortenUrl {get; set;}

        public AppDbContext(DbContextOptions<AppDbContext> options)
            : base(options)
        { }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            var shortenURL = modelBuilder.Entity<ShortenURLViewModel>();
            shortenURL.ToTable("shortenurl");
            shortenURL.HasKey(c => c.Id);
            shortenURL.Property(c => c.OriginalURL).HasColumnType("text");
        }
    }
}