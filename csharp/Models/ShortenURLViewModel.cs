using Newtonsoft.Json;

namespace csharp.Models
{
    public class ShortenURLViewModel
    {
        [JsonProperty("id")]
        public string Id { get; set; }

        [JsonProperty("originalURL")]
        public string OriginalURL { get; set; }
    }
}