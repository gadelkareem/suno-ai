//  open your javascript console and paste this
copy([...$('[role="grid"]')[Object.keys($('[role="grid"]')).filter(x => x.startsWith('__reactProps'))[0]].children[0].props.values[0][1].collection]
    .filter(x => x.value.clip.clip.audio_url || x.value.clip.clip.video_url)
    .map(x => {
        const title = x.value.clip.clip.title.trim() || x.value.clip.clip.id ;
        const audio = x.value.clip.clip.audio_url ? `${title}.mp3|${x.value.clip.clip.audio_url}` : '';
        const video = x.value.clip.clip.video_url ? `${title}.mp4|${x.value.clip.clip.video_url}` : '';
        return [audio, video].filter(Boolean).join("\n");
    })
    .join("\n")
)
// now you have a list of mp3 urls directly in your clipboard that you can pass to wget or a url downloader
