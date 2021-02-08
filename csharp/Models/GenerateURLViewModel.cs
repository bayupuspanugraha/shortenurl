using Newtonsoft.Json;

namespace csharp.Models
{
    public class GenerateURLViewModel
    {
        [JsonProperty("url")]
        public string URL { get; set; }
    }
}