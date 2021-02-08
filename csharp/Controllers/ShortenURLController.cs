using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Nanoid;
using csharp.Models;
using Microsoft.AspNetCore.Mvc;
using csharp.DB;
using System.Linq; 
using Microsoft.EntityFrameworkCore;

namespace csharp.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class ShortenURLController : ControllerBase 
    {
        private string _baseURL = "https://localhost:5001";
        private AppDbContext _appDbContext;

        public ShortenURLController(AppDbContext appDbContext) {
            this._appDbContext = appDbContext;
        }   

        [HttpGet("/")]
        public IList<UrlInfoViewModel> Index()
        {
            IList<UrlInfoViewModel> infosResult = new List<UrlInfoViewModel>() {
                new UrlInfoViewModel {
                    URL = "/info",
                    Method = "GET",
                    Params = "",
                    Body = "",
                    Desc = "Shows all data from database"
                },
                new UrlInfoViewModel {
                    URL = "/shortenurl",
                    Method = "POST",
                    Params = "",
                    Body = "{url: 'YOUR_STRING_URL'}",
                    Desc = "Generates new short url from original url"
                },
                new UrlInfoViewModel {
                    URL = "/go/:id",
                    Method = "GET",
                    Params = ":id => the shorten url id",
                    Body = "",
                    Desc = "Access your ORIGINAL Url and redirect to the page"
                },
                new UrlInfoViewModel {
                    URL = "/swagger",
                    Method = "GET",
                    Params = "",
                    Body = "",
                    Desc = "Swagger access to entire api endpoint"
                },
            }; 
            
            return infosResult;
        }

        [HttpGet("/info")]
        public async Task<IList<InfoViewModel>> GetInfo() 
        {
            var dataList = await this._appDbContext.ShortenUrl.ToListAsync();
            
            return dataList.Select(c => new InfoViewModel {
                OriginalURL = c.OriginalURL,
                ShortURL = $"{this._baseURL}/go/{c.Id}"
            }).ToList();
        }

        [HttpPost("/shortenurl")]
        public async Task<ActionResult<ShortenURLViewModel>> GenerateURL([FromBody]GenerateURLViewModel model)
        {
            if(model == null || string.IsNullOrEmpty(model.URL))
            {
                return BadRequest();
            }   

            var newID = Nanoid.Nanoid.Generate(size:10);
            var newData = new ShortenURLViewModel{
                Id = newID,
                OriginalURL = model.URL
            };

            await this._appDbContext.ShortenUrl.AddAsync(newData);
            await this._appDbContext.SaveChangesAsync();

            return newData; 
        }

        [HttpGet("/go/{id}")]
        public async Task<IActionResult> Go(string id)
        { 
            var targetData = await this._appDbContext.ShortenUrl.FirstOrDefaultAsync(s => s.Id == id);
            if(targetData == null)
            {
                return BadRequest();
            }

            return Redirect(targetData.OriginalURL);
        }
    }
}