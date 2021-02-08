using Newtonsoft.Json;

namespace csharp.Models
{
    public class InfoViewModel
    {
        [JsonProperty("originalURL")]
        public string OriginalURL { get; set; }

        [JsonProperty("shortURL")]
        public string ShortURL { get; set; }
    }
}