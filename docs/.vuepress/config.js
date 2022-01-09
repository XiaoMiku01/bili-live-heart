module.exports = {
    title: '哔哩哔哩粉丝牌助手',
    description: '哔哩哔哩粉丝牌助手',
    base: '/',
    head: [
        ['link', { rel: 'icon', href: '/logo.png' }],
    ],
    themeConfig: {
        logo: '/logo.png',
        repo: 'XiaoMiku01/bili-live-heart',
        nav: [
            { text: 'Home', link: '/' },
            { text: '指南', link: '/guide/' },
        ],
        // search: false,
        sidebar: 'auto',
        editLinkText: '编辑此页',
        editLinks: true,
    }
}

